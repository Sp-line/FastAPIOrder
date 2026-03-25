from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app_types import (
        PriceMap,
        IntMap,
        TicketPricingData
    )
    from core.models import Seat
    from constants import SeatType
    from collections.abc import Iterable


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_ticket_price(
            self,
            session_id: int,
            seat_type: SeatType,
            prices_map: PriceMap
    ) -> Decimal:
        ...

    @abstractmethod
    def calculate_order_price(
            self,
            tickets: Iterable[TicketPricingData],
            seats_map: IntMap[Seat],
            prices_map: PriceMap
    ) -> Decimal:
        ...

    @abstractmethod
    def add_ticket(self, order_total_price: Decimal, new_ticket_price: Decimal) -> Decimal:
        ...

    @abstractmethod
    def remove_ticket(self, order_total_price: Decimal, removed_ticket_price: Decimal) -> Decimal:
        ...

    @abstractmethod
    def update_ticket_price(self, order_total: Decimal, old_price: Decimal, new_price: Decimal) -> Decimal:
        ...


class DefaultPricing(PricingStrategy):
    def calculate_ticket_price(
            self,
            session_id: int,
            seat_type: SeatType,
            prices_map: PriceMap
    ) -> Decimal:
        return prices_map[(session_id, seat_type)].price

    def calculate_order_price(
            self,
            data: Iterable[TicketPricingData],
            seats_map: IntMap[Seat],
            prices_map: PriceMap
    ) -> Decimal:
        total = Decimal("0.00")

        for item in data:
            ticket_price = self.calculate_ticket_price(
                session_id=item.session_id,
                seat_type=seats_map[item.seat_id].type,
                prices_map=prices_map
            )
            total += ticket_price

        return total

    def add_ticket(self, order_total_price: Decimal, new_ticket_price: Decimal) -> Decimal:
        return order_total_price + new_ticket_price

    def remove_ticket(self, order_total_price: Decimal, removed_ticket_price: Decimal) -> Decimal:
        return order_total_price - removed_ticket_price

    def update_ticket_price(
            self,
            order_total_price: Decimal,
            old_ticket_price: Decimal,
            new_ticket_price: Decimal
    ) -> Decimal:
        return order_total_price - old_ticket_price + new_ticket_price
