from importlib import resources

from alembic import command
from alembic.config import Config

with (
    resources.path("todo.db", "alembic.ini") as cfg_path,
    resources.path("todo.db", "migrations") as migrations_path,
):
    alembic_config = Config(cfg_path)
    alembic_config.set_main_option("script_location", str(migrations_path))


def apply_migrations() -> None:
    command.upgrade(alembic_config, "head")
