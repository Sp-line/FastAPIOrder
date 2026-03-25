from dataclasses import dataclass

from domain import EnsureOrderIsSafeToDelete
from services import OrderDataExistenceService


@dataclass(frozen=True, slots=True)
class DeleteOrderDataExistenceServices:
    order: OrderDataExistenceService


@dataclass(frozen=True, slots=True)
class DeleteOrderDomain:
    order_is_safe_to_delete: EnsureOrderIsSafeToDelete
