from datetime import datetime
from typing import Annotated, Optional

from typer import Argument, BadParameter, Option, Typer

from todo.config import settings
from todo.db.management import apply_migrations

app = Typer(no_args_is_help=True)


@app.callback()
def setup() -> None:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.db_file.touch(exist_ok=True)
    apply_migrations()


def title_callback(value: str) -> str:
    if not value.strip():
        raise BadParameter("Only non-empty string is allowed.")
    return value


@app.command()
def add(
    title: Annotated[str, Argument(callback=title_callback, show_default=False)],
    target_date: Annotated[
        Optional[datetime],
        Option(
            "--date",
            "-d",
            formats=["%Y-%m-%d"],
            metavar="YYYY-MM-DD",
            prompt="Date",
            prompt_required=False,
        ),
    ] = None,
) -> None:
    print(title, target_date and target_date.date())
