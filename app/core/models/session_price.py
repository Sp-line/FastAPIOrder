from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import SessionPriceLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Session


class SessionPrice(IntIdPkMixin, Base):
    seat_type: Mapped[str] = mapped_column(String(SessionPriceLimits.SEAT_TYPE_MAX))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"))

    session: Mapped["Session"] = relationship(back_populates="prices")
