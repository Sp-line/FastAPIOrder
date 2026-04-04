"""add inbox_events model

Revision ID: 81bac1337f6f
Revises: 0c7eb566795a
Create Date: 2026-04-03 18:14:59.101834

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "81bac1337f6f"
down_revision: Union[str, None] = "0c7eb566795a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "inbox_events",
        sa.Column("code", sa.UUID(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_inbox_events")),
        sa.UniqueConstraint("code", name=op.f("uq_inbox_events_code")),
    )


def downgrade() -> None:
    op.drop_table("inbox_events")
