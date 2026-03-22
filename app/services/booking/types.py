from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import (
        Session,
        Seat,
        SessionPrice,
        Order
    )
    from constants import SeatType

type SessionPriceCombinationTuple = tuple[int, SeatType]

type OrderMap = dict[int, Order]
type SessionMap = dict[int, Session]
type SeatMap = dict[int, Seat]
type PriceMap = dict[SessionPriceCombinationTuple, SessionPrice]
