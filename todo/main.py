from contextlib import suppress
from dataclasses import dataclass
from datetime import date, datetime
from itertools import count
from typing import Annotated, Optional

from rich.console import Console
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import select
from typer import Argument, BadParameter, Context, Exit, Option, Typer, prompt

from todo.config import dev_settings, settings
from todo.db.core import session_factory
from todo.db.management import apply_migrations
from todo.db.models import Assertion, Space, Task

app = Typer(
    help="Manage your daily tasks directly from the terminal.",
    no_args_is_help=True,
    pretty_exceptions_show_locals=dev_settings.debug,
)
console = Console()

spaces_app = Typer(help="Manage spaces.", no_args_is_help=True)


@spaces_app.command("add", help="Create a new space.", no_args_is_help=True)
def create_space(
    name: Annotated[
        str, Argument(help="Unique name of the space.", show_default=False)
    ],
    *,
    description: Annotated[
        Optional[str],
        Option(
            "--description",
            "-d",
            help="Specify a description for the space.",
            prompt="Description",
            prompt_required=False,
        ),
    ] = None,
) -> None:
    with session_factory() as session:
        new_space = Space(name=name, description=description)
        session.add(new_space)
        session.commit()
        console.print(
            f"Space [magenta]#{new_space.id}[/] was created.", style="bold green"
        )


@spaces_app.command("delete", help="Delete a space.", no_args_is_help=True)
def delete_space(
    space_id: Annotated[
        int,
        Argument(help="ID of the space to delete.", show_default=False),
    ],
) -> None:
    with session_factory() as session:
        space = session.get(Space, space_id)
        if not space:
            console.print(
                f"Space [cyan]#{space_id}[/] does not exist.",
                style="bold red",
            )
            raise Exit(1)

        try:
            session.delete(space)
            session.commit()
        except IntegrityError as exc:
            console.print(exc.orig, style="bold yellow")
            raise Exit from exc
        else:
            console.print(
                f"Task [magenta]#{space.id}[/] was deleted.", style="bold green"
            )


@spaces_app.command("activate", help="Activate a space.", no_args_is_help=True)
def activate_space(
    space_id: Annotated[
        int,
        Argument(help="ID of the space to activate.", show_default=False),
    ],
) -> None:
    with session_factory() as session:
        space = session.get(Space, space_id)
        if not space:
            console.print(
                f"Space [cyan]#{space_id}[/] does not exist.",
                style="bold red",
            )
            raise Exit(1)

        if space.active:
            console.print(
                f"Space [blue]#{space.id}[/] has already been activated.",
                style="bold yellow",
            )
            raise Exit

        space.active = True
        session.commit()
        console.print(
            f"Space [magenta]#{space.id}[/] was activated.", style="bold green"
        )


@spaces_app.command("disable", help="Disable a space.", no_args_is_help=True)
def disable_space(
    space_id: Annotated[
        int,
        Argument(help="ID of the space to disable.", show_default=False),
    ],
) -> None:
    with session_factory() as session:
        space = session.get(Space, space_id)
        if not space:
            console.print(
                f"Space [cyan]#{space_id}[/] does not exist.",
                style="bold red",
            )
            raise Exit(1)

        if space.disabled_at:
            console.print(
                f"Space [blue]#{space.id}[/] has already been disabled.",
                style="bold yellow",
            )
            raise Exit

        else_enabled_spaces_count = (
            session.query(Space)
            .filter(Space.id != space.id, Space.disabled_at == None)  # noqa: E711
            .count()
        )
        if else_enabled_spaces_count == 0:
            console.print("At least one space must be enabled.", style="bold yellow")
            raise Exit

        space.disabled_at = datetime.now()
        session.commit()
        console.print(
            f"Space [magenta]#{space.id}[/] was disabled.", style="bold green"
        )


@spaces_app.command("enable", help="Enable a space.", no_args_is_help=True)
def enable_space(
    space_id: Annotated[
        int,
        Argument(help="ID of the space to enable.", show_default=False),
    ],
) -> None:
    with session_factory() as session:
        space = session.get(Space, space_id)
        if not space:
            console.print(
                f"Space [cyan]#{space_id}[/] does not exist.",
                style="bold red",
            )
            raise Exit(1)

        if not space.disabled_at:
            console.print(
                f"Space [blue]#{space.id}[/] is not disabled.",
                style="bold yellow",
            )
            raise Exit

        space.disabled_at = None
        session.commit()
        console.print(f"Space [magenta]#{space.id}[/] was enabled.", style="bold green")


@spaces_app.command("list", help="List spaces.")
def list_spaces() -> None:
    with session_factory() as session:
        query = select(Space)
        spaces = session.scalars(query)
        for space in spaces:
            console.print(space)


app.add_typer(spaces_app, name="spaces")


@dataclass
class State:
    space_id: int


def get_active_space_id() -> int:
    with session_factory() as session:
        space = session.query(Space).filter_by(active=True).one()
    return space.id


def version_callback(value: bool) -> None:
    if value:
        console.print(f"{settings.project_name} {settings.version}", highlight=False)
        raise Exit


@app.callback()
def setup(
    ctx: Context,
    *,
    _version: Annotated[
        bool, Option("--version", "-v", callback=version_callback, is_eager=True)
    ] = False,
) -> None:
    ctx.obj = State(space_id=get_active_space_id())
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.db_file.touch(exist_ok=True)
    apply_migrations()


def title_callback(value: str) -> str:
    if not value.strip():
        raise BadParameter("Only non-empty string is allowed.")  # noqa: TRY003
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
    raise ValueError(f"'{value}' does not match any of formats: {joined_formats}.")  # noqa: TRY003


def target_date_parser(value: str) -> date:
    # For some reason, Typer calls parser twice on prompt.
    if isinstance(value, date):
        return value

    try:
        return parse_str_to_date(value)
    except ValueError as exc:
        raise BadParameter(str(exc)) from exc


@app.command(help="Create a new task.", no_args_is_help=True)
def add(
    ctx: Context,
    title: Annotated[
        str,
        Argument(
            callback=title_callback,
            help="Title of the task.",
            show_default=False,
        ),
    ],
    *,
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
    prompt_assertions: Annotated[
        bool,
        Option(
            "--assertions",
            "-a",
            help="Prompt for assertions.",
        ),
    ] = False,
) -> None:
    assertion_titles: list[str] = []
    if prompt_assertions:
        console.print("Enter assertions (or 'stop' to finish)")
        for assertion_idx in count(1):
            assertion_input = prompt(str(assertion_idx))
            if assertion_input == "stop":
                break
            assertion_titles.append(assertion_input)

    with session_factory() as session:
        assertions = [
            Assertion(title=assertion_title) for assertion_title in assertion_titles
        ]
        new_task = Task(
            title=title,
            target_date=target_date,
            space_id=ctx.obj.space_id,
            assertions=assertions,
        )
        session.add(new_task)
        session.commit()
        console.print(
            f"Task [magenta]#{new_task.id}[/] was created.", style="bold green"
        )


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
            console.print(f"Task [cyan]#{task_id}[/] does not exist.", style="bold red")
            raise Exit(1)

        if task.completed_at:
            console.print(
                f"Task [blue]#{task.id}[/] has already been completed.",
                style="bold yellow",
            )
        else:
            now = datetime.now()
            task.updated_at = now
            task.completed_at = now
            session.commit()
            console.print(
                f"Task [magenta]#{task.id}[/] was completed.", style="bold green"
            )


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
            console.print(f"Task [cyan]#{task_id}[/] does not exist.", style="bold red")
            raise Exit(1)

        if not task.completed_at:
            console.print(
                f"Task [blue]#{task.id}[/] has not been completed yet.",
                style="bold yellow",
            )
        else:
            task.completed_at = None
            session.commit()
            console.print(
                f"Task [magenta]#{task.id}[/] was uncompleted.", style="bold green"
            )


@app.command(help="Delete a task.", no_args_is_help=True)
def delete(
    task_id: Annotated[
        int,
        Argument(help="ID of the task to delete.", show_default=False),
    ],
) -> None:
    with session_factory() as session:
        task = session.get(Task, task_id)
        if not task:
            console.print(f"Task [cyan]#{task_id}[/] does not exist.", style="bold red")
            raise Exit(1)

        session.delete(task)
        session.commit()
        console.print(f"Task [magenta]#{task.id}[/] was deleted.", style="bold green")


@app.command("list", help="List tasks.")
def list_() -> None:
    with session_factory() as session:
        query = select(Task)
        tasks = session.scalars(query)
        for task in tasks:
            console.print(task)
