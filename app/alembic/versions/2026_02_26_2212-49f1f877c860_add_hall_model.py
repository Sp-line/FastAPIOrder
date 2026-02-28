"""add Hall model

Revision ID: 49f1f877c860
Revises: 16a8b5f06301
Create Date: 2026-02-26 22:12:36.749786

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "49f1f877c860"
down_revision: Union[str, None] = "16a8b5f06301"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "halls",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("slug", sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_halls")),
        sa.UniqueConstraint("slug", name=op.f("uq_halls_slug")),
    )


def downgrade() -> None:
    op.drop_table("halls")
