from importlib import resources

from alembic import command
from alembic.config import Config

db_resources = resources.files("todo.db")
config_path = str(db_resources.joinpath("alembic.ini"))
migrations_path = str(db_resources.joinpath("migrations"))

config = Config(config_path)
config.set_main_option("script_location", migrations_path)


def apply_migrations() -> None:
    command.upgrade(config, "head")
