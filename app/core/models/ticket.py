from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Uuid, ForeignKey, String, Numeric, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import TicketLimits, TicketStatus
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Order, Session, Seat


class Ticket(IntIdPkMixin, Base):
    public_code: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), default=uuid4, unique=True)
    status: Mapped[str] = mapped_column(String(TicketLimits.STATUS_MAX), default=TicketStatus.RESERVED.value, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id", ondelete="RESTRICT"), index=True)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id", ondelete="RESTRICT"), index=True)

    order: Mapped["Order"] = relationship(back_populates="tickets")
    session: Mapped["Session"] = relationship(back_populates="tickets")
    seat: Mapped["Seat"] = relationship(back_populates="tickets")

    snapshot: Mapped[dict] = mapped_column(JSONB)

    __table_args__ = (
        Index(
            "ix_unique_active_ticket_per_seat",
            "session_id", "seat_id",
            unique=True,
            postgresql_where=status.in_(
                {
                    TicketStatus.RESERVED.value,
                    TicketStatus.ACTIVE.value,
                    TicketStatus.USED.value
                }
            )
        ),
    )
