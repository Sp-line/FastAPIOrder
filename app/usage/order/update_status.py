from dataclasses import dataclass

from constants import OrderStatus
from domain import EnsureValidOrderStatusTransition
from repositories import (
    UnitOfWork,
    OrderRepository
)
from schemas.order import (
    OrderStatusUpdateReq,
    OrderRead, OrderUpdateDB
)
from services import OrderDataExistenceService
from services.booking import OrderSchedulerService


@dataclass(frozen=True, slots=True)
class UpdateOrderStatusDataExistenceServices:
    order: OrderDataExistenceService


@dataclass(frozen=True, slots=True)
class UpdateOrderStatusDomain:
    valid_order_status_transition: EnsureValidOrderStatusTransition


class UpdateOrderStatusUsage:
    def __init__(
            self,
            order_repo: OrderRepository,
            unit_of_work: UnitOfWork,

            scheduler: OrderSchedulerService,
            domain: UpdateOrderStatusDomain,
            data_existence: UpdateOrderStatusDataExistenceServices,
    ) -> None:
        self._order_repo = order_repo
        self._uow = unit_of_work

        self._scheduler = scheduler
        self._domain = domain
        self._data_existence = data_existence

    async def __call__(self, order_id: int, data: OrderStatusUpdateReq) -> OrderRead:
        order = self._data_existence.order.ensure_obj_exist(
            obj_id=order_id,
            obj=await self._order_repo.get_by_id(order_id)
        )
        self._domain.valid_order_status_transition(
            current_status=order.status,
            target_status=data.status
        )

        async with self._uow:
            updated_order = await self._order_repo.update(
                obj_id=order.id,
                data=OrderUpdateDB(status=data.status)
            )

            conditions = (
                order.status == OrderStatus.PENDING,
                data.status != OrderStatus.PENDING,
                order.expire_schedule_id
            )
            if all(conditions):
                await self._scheduler.cancel_task(
                    schedule_id=order.expire_schedule_id  # type: ignore[arg-type]
                )

            return OrderRead.model_validate(updated_order)
