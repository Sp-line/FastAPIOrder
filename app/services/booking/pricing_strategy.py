from abc import ABC, abstractmethod
from decimal import Decimal

from schemas.booking import BookingTicketNestedCreateReq
from services.booking.types import PriceMap, SeatMap


class PricingStrategy(ABC):
    @staticmethod
    @abstractmethod
    def calculate(
            tickets: list[BookingTicketNestedCreateReq],
            seats_map: SeatMap,
            prices_map: PriceMap
    ) -> Decimal:
        ...

    @staticmethod
    @abstractmethod
    def increment_by_one(order_total_price: Decimal, new_ticket_price: Decimal) -> Decimal:
        ...

    @staticmethod
    @abstractmethod
    def decrement_by_one(order_total_price: Decimal, removed_ticket_price: Decimal) -> Decimal:
        ...


class DefaultPricing(PricingStrategy):
    @staticmethod
    def calculate(
            tickets: list[BookingTicketNestedCreateReq],
            seats_map: SeatMap,
            prices_map: PriceMap
    ) -> Decimal:
        total = Decimal("0.00")

        for ticket in tickets:
            seat = seats_map[ticket.seat_id]
            price_key = (ticket.session_id, seat.type)
            price = prices_map[price_key]
            total += price.price

        return total

    @staticmethod
    def increment_by_one(order_total_price: Decimal, new_ticket_price: Decimal) -> Decimal:
        return order_total_price + new_ticket_price

    @staticmethod
    def decrement_by_one(order_total_price: Decimal, removed_ticket_price: Decimal) -> Decimal:
        return order_total_price - removed_ticket_price
