from dotenv import load_dotenv
import re
import ast
import json
from groq import Groq
from typing import cast, Any
import typer
from pathlib import Path

load_dotenv()
MAX_CHAR = 15_000
MAX_CUMULATIVE_CHAR = 4_500
MAX_BATCH_SIZE = 3

app = typer.Typer()
def has_documentation(function_string: str) -> bool:
    try:
        tree = ast.parse(function_string.strip(" "))
    except SyntaxError:
        return False

    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            return ast.get_docstring(node) is not None

    return False


def get_funcs(content: str, target: str = "function") -> list[str]:
    if target == "function":
        match_str = r"^(\s*)def\s+\w+\s*\("
    elif target == "class":
        match_str = r"^(\s*)class\s+\w+\s*"
    lines = content.splitlines()
    functions = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Match a function definition, allowing leading whitespace.
        match = re.match(match_str, line)

        if match:
            def_indent = len(match.group(1).expandtabs(4))
            block = [line]
            i += 1

            while i < len(lines):
                current = lines[i]

                # Keep blank lines inside the function.
                if not current.strip():
                    block.append(current)
                    i += 1
                    continue

                current_indent = len(current) - len(current.lstrip())

                # Function ended when we return to the def's indentation
                # or lower.
                if current_indent <= def_indent:
                    break

                block.append(current)
                i += 1

            functions.append("\n".join(block))
            continue

        i += 1

    return functions


def replace_multiline_string(
    original: str,
    larger: str,
    replacement: str
) -> str:
    if original not in larger:
        raise ValueError("Original string was not found in larger string.")

    return larger.replace(original, replacement, 1)


def insert_documentation(function: str, documentation: str) -> str:
    lines = function.splitlines()
    index = 0
    for line in lines:
        if line.lstrip().endswith(":"):
            index = lines.index(line)
            break

    first_indent = lines[index+1]
    indentation = first_indent[:len(first_indent) - len(first_indent.lstrip())]
    documentation = f'"""{documentation}"""'

    documentation = "\n".join(
        indentation + line
        for line in documentation.splitlines()
    )
    if not lines:
        return documentation
    # print("ranr", lines[-1])

    return "\n".join([*lines[:index+1], documentation, *lines[index+1:-1], lines[-1]+"\n"])

def get_class(content: str) -> tuple[list[str], str]:
    functions = get_funcs(content, target="class")
    new_content = content
    for func in functions:
        new_content = replace_multiline_string(func, new_content, "")
    return (functions, new_content)

def get_sub(content: str, target: str):
    # target should be either "function" or "class"
    try:
        next_line = content.index(":")
        functions_ = get_funcs(content[next_line:], target)
        # split_content = content.split("\n", 1)[1]
        # functions_ = get_funcs(split_content, target)
        value = []
        # print(functions)
        for func_ in functions_:
            value.append(func_)
            value.extend(get_sub(func_, target))
    except ValueError:
        return []
    else:
        return value


def parse_source(content: str) -> tuple[str, list[str], dict[Any, Any]]:
    # Read source code
    # with open("app_test.py", mode="r") as py_file:
    #     content = py_file.read()

    # Read classes
    classes, new_content = get_class(content)

    # Read methods and subclasses
    methods = []
    for class_ in classes.copy():
        methods.extend(get_funcs(class_, target="function"))
        sub_classes = get_sub(class_, "class")
        classes.extend(sub_classes)

    # Read functions
    functions = get_funcs(new_content)
    i = 0
    for func in functions.copy():
        sub_func = get_sub(func, "function")
        functions.extend(sub_func)
        i += 1

    pre_filter = []
    pre_filter.extend(classes)
    pre_filter.extend(methods)
    pre_filter.extend(functions)

    filtered = {}
    batched = []
    track = MAX_BATCH_SIZE
    id_ = 0

    for obj in pre_filter:
        if has_documentation(obj):
            pass
            # print("Has doc")
        elif len(obj) > MAX_CHAR:
            print("Function too large!!")
        else:
            if track == MAX_BATCH_SIZE or len(batched[-1]) + len(obj) > MAX_CHAR:
                batched.append(f"obj_{id_}\n{obj}")
                filtered[f"obj_{id_}"] = obj
                track = 1
            else:  # I.e len(batched[-1]) + len(obj) <= MAX_CHAR:
                batched[-1] += f"\n\nobj_{id_}\n{obj}"
                filtered[f"obj_{id_}"] = obj
                track += 1
            id_ += 1
    return content, batched, filtered


def generate_doc(batched_obj: list) -> list[dict[Any, Any] | None]:
    client = Groq()

    system_prompt = """
    You are an excellent senior developer with 15+ years of experience in creating and documenting codes, apis, functions, classes and more.
    Generate industry-standard documentation for the Python (functions, methods, classes, etc) provided below.

    Analyze the function's signature, implementation, parameters, return behavior,
    exceptions, side effects, and overall purpose before writing the documentation.

    Use only information that can be reasonably inferred from the function and its
    implementation. Do not invent behavior, parameters, exceptions, or guarantees
    that are not supported by the code.

    Use the Google documentation style
    Write a complete, accurate, and concise docstring appropriate for production code.

    Return the documentation only. Do not return or reproduce the Python function or include `def func()`).
    Your response should contain the  id of the object the string belongs to, the style and docstring itself as shown in the example below.

    Return the result as a JSON object with exactly these fields:

    [
    {
        "id": "obj_1",
        "style": "Google",
        "docstring": "Prints users desire.\n\nArgs:..."
    },
    .
    .
    ]
    """
    cum_res = []
    for func in batched_obj:
        # noinspection bad-argument-type
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"""
                    Here is the python function to document: {func}"""
                }
            ],
            temperature=0.4,
            max_completion_tokens=4096,
            top_p=1,
            reasoning_effort="medium",
            stream=False,
            stop=None,

            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "documentation_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "string"
                                        },
                                        "style": {
                                            "type": "string"
                                        },
                                        "docstring": {
                                            "type": "string"
                                        }
                                    },
                                    "required": [
                                        "id",
                                        "style",
                                        "docstring"
                                    ],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": [
                            "items"
                        ],
                        "additionalProperties": False
                    }
                }
            }
        )

        response = completion.choices[0].message.content
        res = json.loads(response)
        cum_res.append(res)
    return cum_res


def update_file(llm_res: list, content: str, original: dict, file: Path):
    updated_code = content
    # llm_res = [item for list_ in llm_res for item in list_]
    for res in llm_res:
        for doc in res.get("items", []):
            docs = doc.get("docstring")
            docs = docs.removeprefix('\"\"\"')
            docs = docs[:-2].removesuffix('\"\"\"') + docs[-2:]
            old_obj = original.get(doc.get("id", ""))

            new_func = insert_documentation(cast(str, old_obj), docs)
            updated_code = replace_multiline_string(cast(str, old_obj), updated_code, new_func)
    file.write_text(updated_code, encoding="utf-8")

    # with open("app_test.py", mode="w") as py_file:
    #     py_file.write(updated_code)


@app.command()
def show(typ: str):
    if typ == "func":
        print("THe number of functions found is:", len(2))
    elif typ == "class":
        print("THe number of classes found is:", len(3))

@app.command()
def run(file: Path):
    path = Path(file)
    if not path.exists():
        typer.echo(f"Error: file '{file}' does not exist.", err=True)
        raise typer.Exit(code=1)

    if not path.is_file():
        typer.echo(f"Error: '{file}' is not a file.", err=True)
        raise typer.Exit(code=1)

    try:
        content = path.read_text(encoding="utf-8")
        source_code, batch_obj, obj_dict = parse_source(content)
        documentation = generate_doc(batch_obj)
        update_file(documentation, source_code, obj_dict, path)
    except PermissionError:
        typer.echo(
            f"Error: permission denied when reading/writing '{file}'.",
            err=True
        )
        raise typer.Exit(code=1)
    except Exception as e:
        with open("__error.txt", mode="w") as error_file:
            error_file.write(f"DocDocGo Error:\n\n{str(e)}")



if __name__ == "__main__":
    app()
