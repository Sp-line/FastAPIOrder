from dataclasses import dataclass

from domain import (
    EnsureOrderCanBeModified,
    EnsureSessionIsOpen,
    EnsureSeatValidForSession
)
from services import (
    SeatDataExistenceService,
    SessionDataExistenceService,
    OrderDataExistenceService,
    SessionPriceDataExistenceService
)


@dataclass(frozen=True, slots=True)
class AddTicketToOrderDataExistenceServices:
    seat: SeatDataExistenceService
    session: SessionDataExistenceService
    order: OrderDataExistenceService
    session_price: SessionPriceDataExistenceService


@dataclass(frozen=True, slots=True)
class AddTicketToOrderDomain:
    order_can_be_modified: EnsureOrderCanBeModified
    session_is_open: EnsureSessionIsOpen
    seat_valid_for_session: EnsureSeatValidForSession
