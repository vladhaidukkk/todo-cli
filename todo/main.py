from typing import Annotated

from typer import Argument, Typer

from todo.config import settings
from todo.db.management import apply_migrations

app = Typer(no_args_is_help=True)


@app.callback()
def setup():
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.db_file.touch(exist_ok=True)
    apply_migrations()


@app.command()
def main(name: Annotated[str, Argument()] = "World"):
    print(f"Hello {name}")
