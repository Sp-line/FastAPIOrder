from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.models import Order, Ticket


class OrderTicketAdapter:
    def __init__(self, order: Order, tickets: list[Ticket]):
        self._order = order
        self.tickets = tickets

    def __getattr__(self, item: str) -> Any:
        return getattr(self._order, item)
