"""Create update_active_space trigger.

Revision ID: 15760d5d26d2
Revises: ca66626ab021
Create Date: 2024-06-15 09:35:11.526030+00:00

"""

from collections.abc import Sequence
from typing import Union

from alembic import op

revision: str = "15760d5d26d2"
down_revision: Union[str, None] = "ca66626ab021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TRIGGER update_active_space
        BEFORE UPDATE OF active ON spaces
        WHEN OLD.active = FALSE AND NEW.active = TRUE
        BEGIN
            UPDATE spaces SET active = FALSE WHERE id != NEW.id AND active = TRUE;
        END;
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER update_active_space;")
