from dataclasses import dataclass

from domain import (
    EnsureUserCanCreateOrder,
    EnsureSessionIsOpen,
    EnsureSeatValidForSession
)
from services import (
    SeatDataExistenceService,
    SessionDataExistenceService,
    SessionPriceDataExistenceService
)


@dataclass(frozen=True, slots=True)
class CreateBookingDataExistenceServices:
    seat: SeatDataExistenceService
    session: SessionDataExistenceService
    session_price: SessionPriceDataExistenceService


@dataclass(frozen=True, slots=True)
class CreateBookingDomain:
    user_can_create_order: EnsureUserCanCreateOrder
    session_is_open: EnsureSessionIsOpen
    seat_valid_for_session: EnsureSeatValidForSession