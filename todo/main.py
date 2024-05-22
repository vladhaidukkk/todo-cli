import os
import sys
from pathlib import Path
from typing import Annotated

from typer import Argument, Typer

NAME = "todo"

app = Typer(no_args_is_help=True)


def get_data_dir() -> Path:
    is_win = sys.platform.startswith("win")
    data_home = (
        os.environ.get("LOCALAPPDATA", "~")
        if is_win
        else os.environ.get("XDG_DATA_HOME", "~/.local/share")
    )
    return Path(f"{data_home}/{NAME}").expanduser()


@app.callback()
def setup():
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    db_file = data_dir / "todo.db"
    db_file.touch(exist_ok=True)


@app.command()
def main(name: Annotated[str, Argument()] = "World"):
    print(f"Hello {name}")
