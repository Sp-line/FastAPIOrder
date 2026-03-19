from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Session, Seat, SessionPrice
    from constants import SeatType

type SessionPriceCombinationTuple = tuple[int, SeatType]

type SessionMap = dict[int, Session]
type SeatMap = dict[int, Seat]
type PriceMap = dict[SessionPriceCombinationTuple, SessionPrice]
