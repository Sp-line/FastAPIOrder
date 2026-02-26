from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import SeatLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Hall


class Seat(IntIdPkMixin, Base):
    type: Mapped[str] = mapped_column(String(SeatLimits.TYPE_MAX))

    row_label: Mapped[str] = mapped_column(String(SeatLimits.ROW_LABEL_MAX))
    column_label: Mapped[str] = mapped_column(String(SeatLimits.COLUMN_LABEL_MAX))

    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id", ondelete="CASCADE"))

    hall: Mapped["Hall"] = relationship(back_populates="seats")
