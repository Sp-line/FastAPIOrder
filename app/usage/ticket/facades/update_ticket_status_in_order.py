from dataclasses import dataclass

from domain import EnsureValidTicketStatusTransition, SyncOrderStatusWithTickets
from services import TicketDataExistenceService, OrderDataExistenceService


@dataclass(frozen=True, slots=True)
class UpdateTicketStatusInOrderDataExistenceServices:
    ticket: TicketDataExistenceService
    order: OrderDataExistenceService


@dataclass(frozen=True, slots=True)
class UpdateTicketStatusInOrderDomain:
    valid_ticket_status_transition: EnsureValidTicketStatusTransition
    sync_order_status_with_tickets: SyncOrderStatusWithTickets
