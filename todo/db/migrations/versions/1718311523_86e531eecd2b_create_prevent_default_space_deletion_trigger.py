"""Create prevent_default_space_deletion trigger.

Revision ID: 86e531eecd2b
Revises: c9877c6310fa
Create Date: 2024-06-13 20:45:23.248886+00:00

"""

from collections.abc import Sequence
from typing import Union

from alembic import op

revision: str = "86e531eecd2b"
down_revision: Union[str, None] = "c9877c6310fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TRIGGER prevent_default_space_deletion
        BEFORE DELETE ON spaces
        FOR EACH ROW
        WHEN OLD.id = 1
        BEGIN
            SELECT RAISE(FAIL, 'Deletion of the default space is not allowed.');
        END;
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER prevent_default_space_deletion")
