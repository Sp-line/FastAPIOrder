from __future__ import annotations

from typing import TYPE_CHECKING

from schemas.session_price import SessionPriceCombination

if TYPE_CHECKING:
    from core.models import SessionPrice, Seat
    from app_types import PriceMap, IntMap
    from collections.abc import Iterable
    from typing import Any


class BookingDataAssembler:
    @staticmethod
    def build_prices_map(prices: Iterable[SessionPrice]) -> PriceMap:
        return {(p.session_id, p.seat_type): p for p in prices}

    @staticmethod
    def build_price_conditions(
            data: Iterable[Any],
            seats_map: IntMap[Seat],
    ) -> set[SessionPriceCombination]:
        return {
            SessionPriceCombination(
                session_id=getattr(item, "session_id"),
                seat_type=seats_map[getattr(item, "seat_id")].type
            )
            for item in data
        }
