"""add Session model

Revision ID: 0f0c244d7f3e
Revises: 1c241f73e789
Create Date: 2026-02-26 23:18:07.995011

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0f0c244d7f3e"
down_revision: Union[str, None] = "1c241f73e789"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("dimension_format", sa.String(length=25), nullable=False),
        sa.Column("screen_technology", sa.String(length=25), nullable=False),
        sa.Column("hall_id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hall_id"],
            ["halls.id"],
            name=op.f("fk_sessions_hall_id_halls"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movies.id"],
            name=op.f("fk_sessions_movie_id_movies"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sessions")),
    )


def downgrade() -> None:
    op.drop_table("sessions")
