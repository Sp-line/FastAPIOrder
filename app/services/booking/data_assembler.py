from __future__ import annotations

from typing import TYPE_CHECKING

from schemas.session_price import SessionPriceCombination

if TYPE_CHECKING:
    from core.models import (
        SessionPrice,
        Seat
    )
    from app_types import (
        PriceMap,
        IntMap,
        TicketPricingData
    )
    from collections.abc import Iterable


class BookingDataAssembler:
    @staticmethod
    def build_prices_map(prices: Iterable[SessionPrice]) -> PriceMap:
        return {(p.session_id, p.seat_type): p for p in prices}

    @staticmethod
    def build_price_conditions(
            data: Iterable[TicketPricingData],
            seats_map: IntMap[Seat],
    ) -> set[SessionPriceCombination]:
        return {
            SessionPriceCombination(
                session_id=item.session_id,
                seat_type=seats_map[item.seat_id].type
            )
            for item in data
        }
