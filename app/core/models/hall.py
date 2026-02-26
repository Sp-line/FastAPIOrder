from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import HallLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Seat, Session


class Hall(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(HallLimits.NAME_MAX))
    slug: Mapped[str] = mapped_column(String(HallLimits.SLUG_MAX), unique=True)

    seats: Mapped[list["Seat"]] = relationship(back_populates="hall", cascade="all, delete-orphan")
    sessions: Mapped[list["Session"]] = relationship(back_populates="hall", cascade="all, delete-orphan")
