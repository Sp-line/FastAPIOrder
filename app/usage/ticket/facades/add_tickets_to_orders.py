from dataclasses import dataclass

from domain import (
    EnsureOrderCanBeModified,
    EnsureSessionIsOpen,
    EnsureSeatValidForSession
)
from services import (
    OrderDataExistenceService,
    SeatDataExistenceService,
    SessionDataExistenceService,
    SessionPriceDataExistenceService
)


@dataclass(frozen=True, slots=True)
class AddTicketsToOrdersDataExistenceServices:
    order: OrderDataExistenceService
    seat: SeatDataExistenceService
    session: SessionDataExistenceService
    session_price: SessionPriceDataExistenceService


@dataclass(frozen=True, slots=True)
class AddTicketsToOrdersDomain:
    order_can_be_modified: EnsureOrderCanBeModified
    session_is_open: EnsureSessionIsOpen
    seat_valid_for_session: EnsureSeatValidForSession
