from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Order, Ticket
    from typing import Any
    from collections.abc import Iterable


class OrderTicketAdapter:
    def __init__(self, order: Order, tickets: Iterable[Ticket]):
        self._order = order
        self.tickets = tickets

    def __getattr__(self, item: str) -> Any:
        return getattr(self._order, item)
