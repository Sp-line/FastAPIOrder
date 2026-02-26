"""add Seat model

Revision ID: 1c241f73e789
Revises: 49f1f877c860
Create Date: 2026-02-26 22:28:36.673415

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "1c241f73e789"
down_revision: Union[str, None] = "49f1f877c860"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "seats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(length=30), nullable=False),
        sa.Column("row_label", sa.String(length=10), nullable=False),
        sa.Column("column_label", sa.String(length=10), nullable=False),
        sa.Column("hall_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hall_id"],
            ["halls.id"],
            name=op.f("fk_seats_hall_id_halls"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_seats")),
    )


def downgrade() -> None:
    op.drop_table("seats")
