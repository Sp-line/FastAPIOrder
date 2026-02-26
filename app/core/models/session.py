from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import SessionLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Hall, Movie, SessionPrice


class Session(IntIdPkMixin, Base):
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    dimension_format: Mapped[str] = mapped_column(String(SessionLimits.DIMENSION_FORMAT_MAX))
    screen_technology: Mapped[str] = mapped_column(String(SessionLimits.SCREEN_TECHNOLOGY_MAX))

    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id", ondelete="RESTRICT"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="RESTRICT"))

    hall: Mapped["Hall"] = relationship(back_populates="sessions")
    movie: Mapped["Movie"] = relationship(back_populates="sessions")

    prices: Mapped[list["SessionPrice"]] = relationship(back_populates="session", cascade="all, delete-orphan")
