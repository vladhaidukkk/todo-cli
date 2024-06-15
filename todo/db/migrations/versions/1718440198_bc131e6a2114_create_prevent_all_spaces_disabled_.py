"""Create prevent_all_spaces_disabled trigger.

Revision ID: bc131e6a2114
Revises: aab35dba9fe9
Create Date: 2024-06-15 08:29:58.492094+00:00

"""

from collections.abc import Sequence
from typing import Union

from alembic import op

revision: str = "bc131e6a2114"
down_revision: Union[str, None] = "aab35dba9fe9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TRIGGER prevent_all_spaces_disabled
        BEFORE UPDATE OF disabled_at ON spaces
        WHEN NEW.disabled_at IS NOT NULL
        BEGIN
            SELECT RAISE(FAIL, 'Cannot disable the last enabled space.')
            WHERE (SELECT COUNT(*) FROM spaces WHERE disabled_at is NULL AND id != NEW.id) = 0;
        END;
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER prevent_all_spaces_disabled")
