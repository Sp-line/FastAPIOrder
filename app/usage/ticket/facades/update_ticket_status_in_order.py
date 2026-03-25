from dataclasses import dataclass

from domain import EnsureValidTicketStatusTransition
from services import TicketDataExistenceService


@dataclass(frozen=True, slots=True)
class UpdateTicketStatusInOrderDataExistenceServices:
    ticket: TicketDataExistenceService


@dataclass(frozen=True, slots=True)
class UpdateTicketStatusInOrderDomain:
    valid_ticket_status_transition: EnsureValidTicketStatusTransition