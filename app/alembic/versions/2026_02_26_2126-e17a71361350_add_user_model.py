"""add User model

Revision ID: e17a71361350
Revises:
Create Date: 2026-02-26 21:26:44.520002

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "e17a71361350"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint(
            "phone_number", name=op.f("uq_users_phone_number")
        ),
    )


def downgrade() -> None:
    op.drop_table("users")
