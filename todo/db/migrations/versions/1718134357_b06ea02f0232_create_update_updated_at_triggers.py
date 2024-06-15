"""Create update_updated_at triggers for existing tables.

Revision ID: b06ea02f0232
Revises: 6a552b8933bb
Create Date: 2024-06-11 19:32:37.732026+00:00

"""

from collections.abc import Sequence
from typing import Union

from alembic import op

revision: str = "b06ea02f0232"
down_revision: Union[str, None] = "6a552b8933bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

existing_tables = ("spaces", "tasks", "assertions")


def upgrade() -> None:
    for table in existing_tables:
        op.execute(
            f"""
            CREATE TRIGGER update_{table}_updated_at
            BEFORE UPDATE ON {table}
            BEGIN
                UPDATE {table} SET updated_at = CURRENT_TIMESTAMP
                WHERE rowid = NEW.rowid;
            END;
            """
        )


def downgrade() -> None:
    for table in existing_tables:
        op.execute(f"DROP TRIGGER update_{table}_updated_at;")
