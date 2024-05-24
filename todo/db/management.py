from alembic import command
from alembic.config import Config

alembic_config = Config("alembic.ini")


def apply_migrations() -> None:
    command.upgrade(alembic_config, "head")
