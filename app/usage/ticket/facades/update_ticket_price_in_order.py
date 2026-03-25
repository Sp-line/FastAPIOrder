from dataclasses import dataclass

from domain import (
    EnsureOrderIsPendingForPriceChange,
    EnsureTicketIsReservedForPriceChange
)
from services import (
    TicketDataExistenceService,
    OrderDataExistenceService
)


@dataclass(frozen=True, slots=True)
class UpdateTicketPriceInOrderDataExistenceServices:
    ticket: TicketDataExistenceService
    order: OrderDataExistenceService


@dataclass(frozen=True, slots=True)
class UpdateTicketPriceInOrderDomain:
    order_is_pending_for_price_change: EnsureOrderIsPendingForPriceChange
    ticket_is_reserved_for_price_change: EnsureTicketIsReservedForPriceChange
