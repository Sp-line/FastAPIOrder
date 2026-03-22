from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING

from constants import OrderStatus
from domain import EnsureOrderCanBeModified
from repositories import (
    OrderRepository,
    TicketRepository,
    UnitOfWork,
)
from schemas.order import (
    OrderRead,
    OrderUpdateDB
)
from services import (
    OrderDataExistenceService,
    TicketDataExistenceService
)
from services.booking import PricingStrategy

if TYPE_CHECKING:
    from core.models import Order


@dataclass(frozen=True, slots=True)
class RemoveTicketFromOrderDataExistenceServices:
    ticket: TicketDataExistenceService
    order: OrderDataExistenceService


@dataclass(frozen=True, slots=True)
class RemoveTicketFromOrderDomain:
    order_can_be_modified: EnsureOrderCanBeModified


class RemoveTicketFromOrderUsage:
    def __init__(
            self,
            order_repo: OrderRepository,
            ticket_repo: TicketRepository,
            unit_of_work: UnitOfWork,

            domain: RemoveTicketFromOrderDomain,
            pricing: PricingStrategy,

            data_existence_services: RemoveTicketFromOrderDataExistenceServices,
    ) -> None:
        self._order_repo = order_repo
        self._ticket_repo = ticket_repo
        self._uow = unit_of_work

        self._domain = domain
        self._pricing = pricing

        self._data_existence_services = data_existence_services

    async def __call__(self, ticket_id: int) -> OrderRead:
        ticket = self._data_existence_services.ticket.ensure_obj_exist(
            obj=await self._ticket_repo.get_by_id(ticket_id),
            obj_id=ticket_id,
        )

        order = self._data_existence_services.order.ensure_obj_exist(
            await self._order_repo.get_by_id(ticket.order_id),
            obj_id=ticket.order_id,
        )
        self._ensure_order_can_be_modified(order)

        new_total_price = self._pricing.decrement_by_one(
            order_total_price=order.total_price,
            removed_ticket_price=ticket.price
        )

        zero_price = Decimal("0.00")

        if new_total_price <= zero_price:
            update_data = OrderUpdateDB(
                total_price=zero_price,
                status=OrderStatus.CANCELED
            )
        else:
            update_data = OrderUpdateDB(total_price=new_total_price)

        async with self._uow:
            await self._ticket_repo.delete(ticket.id)

            updated_order = await self._order_repo.update(
                obj_id=order.id,
                data=update_data,
            )

            return OrderRead.model_validate(updated_order)

    def _ensure_order_can_be_modified(self, order: Order) -> None:
        self._domain.order_can_be_modified(
            order_status=order.status,
        )
