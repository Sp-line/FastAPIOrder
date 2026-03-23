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
    def add_ticket(order_total_price: Decimal, new_ticket_price: Decimal) -> Decimal:
        ...

    @staticmethod
    @abstractmethod
    def remove_ticket(order_total_price: Decimal, removed_ticket_price: Decimal) -> Decimal:
        ...

    @staticmethod
    @abstractmethod
    def update_ticket_price(order_total: Decimal, old_price: Decimal, new_price: Decimal) -> Decimal:
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
    def add_ticket(order_total_price: Decimal, new_ticket_price: Decimal) -> Decimal:
        return order_total_price + new_ticket_price

    @staticmethod
    def remove_ticket(order_total_price: Decimal, removed_ticket_price: Decimal) -> Decimal:
        return order_total_price - removed_ticket_price

    @staticmethod
    def update_ticket_price(
            order_total_price: Decimal,
            old_ticket_price: Decimal,
            new_ticket_price: Decimal
    ) -> Decimal:
        return order_total_price - old_ticket_price + new_ticket_price
