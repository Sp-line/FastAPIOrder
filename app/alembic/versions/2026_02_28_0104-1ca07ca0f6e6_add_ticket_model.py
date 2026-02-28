"""add Ticket model

Revision ID: 1ca07ca0f6e6
Revises: 4583eb3bcdd5
Create Date: 2026-02-28 01:04:27.368114

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "1ca07ca0f6e6"
down_revision: Union[str, None] = "4583eb3bcdd5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tickets",
        sa.Column("public_code", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("seat_id", sa.Integer(), nullable=False),
        sa.Column(
            "snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
            name=op.f("fk_tickets_order_id_orders"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["seat_id"],
            ["seats.id"],
            name=op.f("fk_tickets_seat_id_seats"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["sessions.id"],
            name=op.f("fk_tickets_session_id_sessions"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tickets")),
        sa.UniqueConstraint(
            "public_code", name=op.f("uq_tickets_public_code")
        ),
    )
    op.create_index(
        op.f("ix_tickets_order_id"), "tickets", ["order_id"], unique=False
    )
    op.create_index(
        op.f("ix_tickets_seat_id"), "tickets", ["seat_id"], unique=False
    )
    op.create_index(
        op.f("ix_tickets_session_id"), "tickets", ["session_id"], unique=False
    )
    op.create_index(
        op.f("ix_tickets_status"), "tickets", ["status"], unique=False
    )
    op.create_index(
        "ix_unique_active_ticket_per_seat",
        "tickets",
        ["session_id", "seat_id"],
        unique=True,
        postgresql_where=sa.text("status IN ('reserved', 'used', 'active')"),
    )


def downgrade() -> None:
    op.drop_index(
        "ix_unique_active_ticket_per_seat",
        table_name="tickets",
        postgresql_where=sa.text("status IN ('reserved', 'used', 'active')"),
    )
    op.drop_index(op.f("ix_tickets_status"), table_name="tickets")
    op.drop_index(op.f("ix_tickets_session_id"), table_name="tickets")
    op.drop_index(op.f("ix_tickets_seat_id"), table_name="tickets")
    op.drop_index(op.f("ix_tickets_order_id"), table_name="tickets")
    op.drop_table("tickets")
