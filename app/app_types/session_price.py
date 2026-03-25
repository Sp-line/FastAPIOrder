from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from constants import SeatType
    from core.models import SessionPrice

type SessionPriceCombinationTuple = tuple[int, SeatType]

type PriceMap = dict[SessionPriceCombinationTuple, SessionPrice]


class TicketPricingData(Protocol):
    session_id: int
    seat_id: int
