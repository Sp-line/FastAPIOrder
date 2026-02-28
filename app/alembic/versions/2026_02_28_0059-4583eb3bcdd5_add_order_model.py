"""add Order model

Revision ID: 4583eb3bcdd5
Revises: e12d352bba62
Create Date: 2026-02-28 00:59:43.920059

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4583eb3bcdd5"
down_revision: Union[str, None] = "e12d352bba62"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.Uuid(), nullable=False),
        sa.Column("public_code", sa.String(length=6), nullable=False),
        sa.Column("status", sa.String(length=25), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expire_schedule_id", sa.String(length=255), nullable=True),
        sa.Column(
            "total_price", sa.Numeric(precision=10, scale=2), nullable=False
        ),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_orders_user_id_users"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
        sa.UniqueConstraint(
            "expire_schedule_id", name=op.f("uq_orders_expire_schedule_id")
        ),
        sa.UniqueConstraint("number", name=op.f("uq_orders_number")),
        sa.UniqueConstraint("public_code", name=op.f("uq_orders_public_code")),
    )
    op.create_index(
        op.f("ix_orders_expires_at"), "orders", ["expires_at"], unique=False
    )
    op.create_index(
        op.f("ix_orders_status"), "orders", ["status"], unique=False
    )
    op.create_index(
        op.f("ix_orders_user_id"), "orders", ["user_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_orders_user_id"), table_name="orders")
    op.drop_index(op.f("ix_orders_status"), table_name="orders")
    op.drop_index(op.f("ix_orders_expires_at"), table_name="orders")
    op.drop_table("orders")
