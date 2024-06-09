from contextlib import suppress
from datetime import date, datetime
from typing import Annotated, Optional

from typer import Argument, BadParameter, Exit, Option, Typer

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


def parse_str_to_date(value: str, formats: Optional[list[str]] = None) -> date:
    formats = formats or ["%Y-%m-%d", "%m-%d", "%d"]

    for fmt in formats:
        with suppress(ValueError):
            parsed = datetime.strptime(value, fmt).date()
            now = datetime.now()
            if "%Y" not in fmt:
                parsed = parsed.replace(year=now.year)
            if "%m" not in fmt:
                parsed = parsed.replace(month=now.month)
            return parsed

    joined_formats = ", ".join(f"'{fmt}'" for fmt in formats)
    raise ValueError(f"'{value}' does not match any of formats: {joined_formats}.")


def target_date_parser(value: str) -> date:
    # For some reason, Typer calls parser twice on prompt.
    if isinstance(value, date):
        return value

    try:
        return parse_str_to_date(value)
    except ValueError as exc:
        raise BadParameter(str(exc))


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
        task = session.get(Task, task_id)
        if not task:
            print(f"Task #{task_id} does not exist.")
            raise Exit(1)

        if task.completed_at:
            print(f"Task #{task.id} has already been completed.")
        else:
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
        task = session.get(Task, task_id)
        if not task:
            print(f"Task #{task_id} does not exist.")
            raise Exit(1)

        if not task.completed_at:
            print(f"Task #{task.id} has not been completed yet.")
        else:
            task.completed_at = None
            session.commit()
            print(f"Task #{task.id} was uncompleted.")


@app.command(help="Delete a task.", no_args_is_help=True)
def delete(
    task_id: Annotated[
        int,
        Argument(help="ID of the task to delete.", show_default=False),
    ]
) -> None:
    with session_factory() as session:
        task = session.get(Task, task_id)
        if not task:
            print(f"Task #{task_id} does not exist.")
            raise Exit(1)
        else:
            session.delete(task)
            session.commit()
            print(f"Task #{task.id} was deleted.")
