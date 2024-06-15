"""Create active_space_change trigger.

Revision ID: d85183396ef7
Revises: 9e131aab3069
Create Date: 2024-06-15 14:50:31.468733+00:00

"""

from collections.abc import Sequence
from typing import Union

from alembic import op

revision: str = "d85183396ef7"
down_revision: Union[str, None] = "9e131aab3069"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TRIGGER active_space_change
        AFTER UPDATE OF active ON spaces
        WHEN OLD.active != NEW.active
        BEGIN
            INSERT INTO spaces_history (space_id, active_status, changed_at)
            VALUES (NEW.id, NEW.active, CURRENT_TIMESTAMP);
        END;
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER active_space_change;")
