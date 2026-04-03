"""add outbox_events model

Revision ID: 0c7eb566795a
Revises: 1ca07ca0f6e6
Create Date: 2026-04-02 22:04:28.513227

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0c7eb566795a"
down_revision: Union[str, None] = "1ca07ca0f6e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "outbox_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.UUID(), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column(
            "payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_outbox_events")),
        sa.UniqueConstraint("code", name=op.f("uq_outbox_events_code")),
    )


def downgrade() -> None:
    op.drop_table("outbox_events")
