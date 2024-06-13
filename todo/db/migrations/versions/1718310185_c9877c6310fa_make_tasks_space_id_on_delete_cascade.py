"""Make tasks space_id foreign key on delete cascade.

Revision ID: c9877c6310fa
Revises: b06ea02f0232
Create Date: 2024-06-13 20:23:05.276861+00:00

"""

from collections.abc import Sequence
from typing import Union

from alembic import op

revision: str = "c9877c6310fa"
down_revision: Union[str, None] = "b06ea02f0232"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("tasks", recreate="always") as batch_op:
        # ### commands auto generated by Alembic - please adjust! ###
        batch_op.drop_constraint("fk_tasks_space_id_spaces", type_="foreignkey")
        batch_op.create_foreign_key(
            op.f("fk_tasks_space_id_spaces"),
            "spaces",
            ["space_id"],
            ["id"],
            ondelete="CASCADE",
        )
        # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table("tasks", recreate="always") as batch_op:
        # ### commands auto generated by Alembic - please adjust! ###
        batch_op.drop_constraint(op.f("fk_tasks_space_id_spaces"), type_="foreignkey")
        batch_op.create_foreign_key(
            "fk_tasks_space_id_spaces", "spaces", ["space_id"], ["id"]
        )
        # ### end Alembic commands ###