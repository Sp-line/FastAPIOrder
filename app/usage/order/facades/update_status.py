from dataclasses import dataclass

from domain import EnsureValidOrderStatusTransition
from services import OrderDataExistenceService


@dataclass(frozen=True, slots=True)
class UpdateOrderStatusDataExistenceServices:
    order: OrderDataExistenceService


@dataclass(frozen=True, slots=True)
class UpdateOrderStatusDomain:
    valid_order_status_transition: EnsureValidOrderStatusTransition
