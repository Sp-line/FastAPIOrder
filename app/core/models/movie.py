from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import MovieLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Session


class Movie(IntIdPkMixin, Base):
    slug: Mapped[str] = mapped_column(String(MovieLimits.SLUG_MAX), unique=True)
    title: Mapped[str] = mapped_column(String(MovieLimits.TITLE_MAX))

    sessions: Mapped[list["Session"]] = relationship(back_populates="movie", cascade="all, delete-orphan")