from dotenv import load_dotenv
import re
import ast
from groq import Groq

load_dotenv()


def has_documentation(function_string: str) -> bool:
    print(function_string[:15], end=" ")
    try:
        tree = ast.parse(function_string.strip(" "))
    except SyntaxError:
        print("\n", function_string)
        print("Syntax Error")
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

    return "\n".join([*lines[:index+1], documentation, *lines[index+1:]])

def get_class(content: str) -> tuple[list[str], str]:
    functions = get_funcs(content, target="class")
    new_content = content
    for func in functions:
        new_content = replace_multiline_string(func, new_content, "")
    return (functions, new_content)

# Read source code
with open("app_test.py", mode="r") as py_file:
    content = py_file.read()
    # print(content)

# Read classes
classes, new_content = get_class(content)

# Read methods
methods = []
for class_ in classes:
    methods.extend(get_funcs(class_, target="function"))
# print(methods)

# Read functions
funcions = get_funcs(new_content)

pre_filter = []
pre_filter.extend(classes)
pre_filter.extend(methods)
pre_filter.extend(funcions)

filtered = []
for obj in pre_filter:
    if has_documentation(obj):
        print("Has doc")
        continue
    filtered.append(obj)
with open("notes.txt", mode="w") as notes:
    for i in filtered:
        notes.write(i)

client = Groq()

system_prompt =  """
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

Return the result as a JSON object with exactly these fields:

{
    "style": "Google",
    "docstring": "Prints users desire.\n\nArgs:..."
}
"""

# print(len(funcs))
updated_code = content


for func in filtered:
    # print(func)
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
        max_completion_tokens=2048,
        top_p=1,
        reasoning_effort="medium",
        stream=False,
        stop=None
    )

    response = completion.choices[0].message.content
    print(response)
    res = ast.literal_eval(response)

    docs = res.get("docstring")
    docs = docs.removeprefix('\"\"\"')
    docs = docs[:-2].removesuffix('\"\"\"') + docs[-2:]

    new_func = insert_documentation(func, docs)
    updated_code = replace_multiline_string(func, updated_code, new_func)
    # print(func)
    # print(new_func)
    # print(updated_code)
    # break

# print(new_func)
# print("---------------------")
# print(updated_code)
with open("app_test.py", mode="w") as py_file:
    py_file.write(updated_code)

