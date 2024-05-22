from typing import Annotated

from typer import Argument, Typer

from todo.config import config

app = Typer(no_args_is_help=True)


@app.callback()
def setup():
    config.data_dir.mkdir(parents=True, exist_ok=True)
    config.db_file.touch(exist_ok=True)


@app.command()
def main(name: Annotated[str, Argument()] = "World"):
    print(f"Hello {name}")
