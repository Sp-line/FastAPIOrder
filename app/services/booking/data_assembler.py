from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING

from core.models.mixins.int_id_pk import IntIdPkMixin
from schemas.booking import BookingTicketNestedCreateReq
from schemas.session_price import SessionPriceCombination

if TYPE_CHECKING:
    from core.models import SessionPrice
    from services.booking.types import SeatMap, PriceMap


class BookingDataAssembler:
    @staticmethod
    def build_map[TModel: IntIdPkMixin](data: Iterable[TModel]) -> dict[int, TModel]:
        return {item.id: item for item in data}

    @staticmethod
    def build_prices_map(prices: Iterable[SessionPrice]) -> PriceMap:
        return {(p.session_id, p.seat_type): p for p in prices}

    @staticmethod
    def build_price_conditions(
            tickets: list[BookingTicketNestedCreateReq],
            seats_map: SeatMap
    ) -> set[SessionPriceCombination]:
        return {
            SessionPriceCombination(
                session_id=t.session_id,
                seat_type=seats_map[t.seat_id].type
            )
            for t in tickets
        }

    @staticmethod
    def get_ids(field: str, data: list[BookingTicketNestedCreateReq]) -> set[int]:
        return {getattr(item, field) for item in data}
