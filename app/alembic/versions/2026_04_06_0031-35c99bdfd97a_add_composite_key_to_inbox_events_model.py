"""add composite key to inbox events model

Revision ID: 35c99bdfd97a
Revises: 81bac1337f6f
Create Date: 2026-04-06 00:31:50.642261

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "35c99bdfd97a"
down_revision: Union[str, None] = "81bac1337f6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "inbox_events",
        sa.Column("handler", sa.String(length=255), nullable=False),
    )
    op.drop_constraint(
        op.f("uq_inbox_events_code"), "inbox_events", type_="unique"
    )
    op.create_unique_constraint(
        "uq_inbox_events_code_handler", "inbox_events", ["code", "handler"]
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_inbox_events_code_handler", "inbox_events", type_="unique"
    )
    op.create_unique_constraint(
        op.f("uq_inbox_events_code"),
        "inbox_events",
        ["code"],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_column("inbox_events", "handler")
