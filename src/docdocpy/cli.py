import typer
from enum import Enum
from pathlib import Path
from dotenv import load_dotenv
from docdocpy.config import get_api_key, save_api_key
from docdocpy.logic import parse_source, generate_doc, update_file

load_dotenv()

app = typer.Typer()


class SizeOptions(str, Enum):
    MEDIUM = "minimal"
    DEFAULT = "default"


def get_or_create_api_key() -> str:
    api_key = get_api_key()

    if api_key:
        return api_key

    typer.echo("DocGo needs an API key to work.")
    api_key = typer.prompt("Enter your Groq API key", hide_input=True)

    save_api_key(api_key)

    typer.echo("✓ Groq API key saved.")

    return api_key


@app.command()
def show(typ: str):
    if typ == "func":
        print("THe number of functions found is:", len(2))
    elif typ == "class":
        print("THe number of classes found is:", len(3))

@app.callback(invoke_without_command=True)
def run(
        ctx: typer.Context,
        file: Path,
        size: SizeOptions = typer.Option(
            SizeOptions.DEFAULT,
            help="The processing size constraint for the file parsing window."
        )
):
    path = Path(file)
    if not path.exists():
        typer.echo(ctx.get_help())
        return
        # typer.echo(f"Error: file '{file}' does not exist.", err=True)
        # raise typer.Exit(code=1)

    if not path.is_file():
        typer.echo(f"Error: '{file}' is not a file.", err=True)
        raise typer.Exit(code=1)
    if size.lower() != "minimal":
        size = "default"

    try:
        api_key = get_or_create_api_key()
        content = path.read_text(encoding="utf-8")
        source_code, batch_obj, obj_dict = parse_source(content)
        documentation = generate_doc(api_key, batch_obj, size)
        update_file(documentation, source_code, obj_dict, path)
        print("Success")
    except PermissionError:
        typer.echo(
            f"Error: permission denied when reading/writing '{file}'.",
            err=True
        )
        raise typer.Exit(code=1)
    # except Exception as e:
    #     with open("__error.txt", mode="w") as error_file:
    #         error_file.write(f"docdocpy Error:\n\n{str(e)}")
    #     raise typer.Exit(code=1)



if __name__ == "__main__":
    app()
