"""add SessionPrice model

Revision ID: e12d352bba62
Revises: 0f0c244d7f3e
Create Date: 2026-02-26 23:44:20.371797

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "e12d352bba62"
down_revision: Union[str, None] = "0f0c244d7f3e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "session_prices",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("seat_type", sa.String(length=30), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["sessions.id"],
            name=op.f("fk_session_prices_session_id_sessions"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_session_prices")),
    )


def downgrade() -> None:
    op.drop_table("session_prices")
