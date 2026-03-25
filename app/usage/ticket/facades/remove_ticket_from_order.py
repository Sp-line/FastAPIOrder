from dataclasses import dataclass

from domain import EnsureOrderCanBeModified
from services import (
    TicketDataExistenceService,
    OrderDataExistenceService
)


@dataclass(frozen=True, slots=True)
class RemoveTicketFromOrderDataExistenceServices:
    ticket: TicketDataExistenceService
    order: OrderDataExistenceService


@dataclass(frozen=True, slots=True)
class RemoveTicketFromOrderDomain:
    order_can_be_modified: EnsureOrderCanBeModified
