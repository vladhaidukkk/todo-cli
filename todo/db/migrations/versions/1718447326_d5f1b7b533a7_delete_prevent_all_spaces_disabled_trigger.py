"""Delete prevent_all_spaces_disabled trigger.

Revision ID: d5f1b7b533a7
Revises: 15760d5d26d2
Create Date: 2024-06-15 10:28:46.587177+00:00

"""

from collections.abc import Sequence
from typing import Union

from alembic import op

revision: str = "d5f1b7b533a7"
down_revision: Union[str, None] = "15760d5d26d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DROP TRIGGER prevent_all_spaces_disabled;")


def downgrade() -> None:
    op.execute(
        """
        CREATE TRIGGER prevent_all_spaces_disabled
        BEFORE UPDATE OF disabled_at ON spaces
        WHEN NEW.disabled_at IS NOT NULL
        BEGIN
            SELECT RAISE(FAIL, 'Cannot disable the last enabled space.')
            WHERE (SELECT COUNT(*) FROM spaces WHERE disabled_at IS NULL AND id != NEW.id) = 0;
        END;
        """
    )
