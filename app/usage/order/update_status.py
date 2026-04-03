from constants import OrderStatus
from repositories import (
    OrderRepository,
    UnitOfWork
)
from schemas.order import (
    OrderStatusUpdateReq,
    OrderUpdateDB,
    OrderAdminRead
)
from services import TaskScheduler
from usage.order.facades import (
    UpdateOrderStatusDomain,
    UpdateOrderStatusDataExistenceServices
)


class UpdateOrderStatusUsage:
    def __init__(
            self,
            order_repo: OrderRepository,
            unit_of_work: UnitOfWork,

            scheduler: TaskScheduler,
            domain: UpdateOrderStatusDomain,
            data_existence: UpdateOrderStatusDataExistenceServices,
    ) -> None:
        self._order_repo = order_repo
        self._uow = unit_of_work

        self._scheduler = scheduler
        self._domain = domain
        self._data_existence = data_existence

    async def __call__(self, order_id: int, data: OrderStatusUpdateReq) -> OrderAdminRead:
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
                await self._scheduler.cancel_schedule(
                    schedule_id=order.expire_schedule_id  # type: ignore[arg-type]
                )

            return OrderAdminRead.model_validate(updated_order)
