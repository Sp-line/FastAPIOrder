"""add Movie model

Revision ID: 16a8b5f06301
Revises: e17a71361350
Create Date: 2026-02-26 21:55:56.925760

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "16a8b5f06301"
down_revision: Union[str, None] = "e17a71361350"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_movies")),
        sa.UniqueConstraint("slug", name=op.f("uq_movies_slug")),
    )


def downgrade() -> None:
    op.drop_table("movies")
