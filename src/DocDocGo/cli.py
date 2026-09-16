import typer
from pathlib import Path
from dotenv import load_dotenv
from logic import parse_source, generate_doc, update_file

load_dotenv()

app = typer.Typer()


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
        print("Success")
    except PermissionError:
        typer.echo(
            f"Error: permission denied when reading/writing '{file}'.",
            err=True
        )
        raise typer.Exit(code=1)
    # except Exception as e:
    #     with open("__error.txt", mode="w") as error_file:
    #         error_file.write(f"DocDocGo Error:\n\n{str(e)}")
    #     raise typer.Exit(code=1)



if __name__ == "__main__":
    app()
