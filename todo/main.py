from contextlib import suppress
from datetime import date, datetime
from typing import Annotated, Optional

from typer import Argument, BadParameter, Option, Typer

from todo.config import dev_settings, settings
from todo.db.core import session_factory
from todo.db.management import apply_migrations
from todo.db.models import Task

app = Typer(
    help="Manage your daily tasks directly from the terminal.",
    no_args_is_help=True,
    pretty_exceptions_show_locals=dev_settings.debug,
)


@app.callback()
def setup() -> None:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.db_file.touch(exist_ok=True)
    apply_migrations()


def title_callback(value: str) -> str:
    if not value.strip():
        raise BadParameter("Only non-empty string is allowed.")
    return value


def target_date_parser(value: str) -> date | None:
    # For some reason, Typer calls parser twice on prompt.
    if isinstance(value, date) or value is None:
        return value

    now = datetime.now()
    parsed: date | None = None

    for fmt in ["%Y-%m-%d", "%m-%d", "%d"]:
        with suppress(ValueError):
            parsed = datetime.strptime(value, fmt).date()
            if "%Y" not in fmt:
                parsed = parsed.replace(year=now.year)
            if "%m" not in fmt:
                parsed = parsed.replace(month=now.month)
            break

    if not parsed:
        raise BadParameter("Date format is invalid.")
    return parsed


@app.command(help="Create a new task.", no_args_is_help=True)
def add(
    title: Annotated[
        str,
        Argument(
            callback=title_callback,
            help="Title of the task.",
            show_default=False,
        ),
    ],
    target_date: Annotated[
        Optional[date],
        Option(
            "--date",
            "-d",
            parser=target_date_parser,
            metavar="[YYYY-MM-DD|MM-DD|DD]",
            help="Specify a target date for the task.",
            prompt="Date",
            prompt_required=False,
        ),
    ] = None,
) -> None:
    with session_factory() as session:
        new_task = Task(title=title, target_date=target_date)
        session.add(new_task)
        session.commit()
        print(f"Task #{new_task.id} was created.")


@app.command(help="Mark a task as completed.", no_args_is_help=True)
def complete(
    task_id: Annotated[
        int,
        Argument(help="ID of the task to complete.", show_default=False),
    ],
) -> None:
    with session_factory() as session:
        task = session.get_one(Task, task_id)
        now = datetime.now()
        task.updated_at = now
        task.completed_at = now
        session.commit()
        print(f"Task #{task.id} was completed.")


@app.command(help="Mark a task as uncompleted.", no_args_is_help=True)
def uncomplete(
    task_id: Annotated[
        int,
        Argument(help="ID of the task to uncomplete.", show_default=False),
    ],
) -> None:
    with session_factory() as session:
        task = session.get_one(Task, task_id)
        task.completed_at = None
        session.commit()
        print(f"Task #{task.id} was uncompleted.")
