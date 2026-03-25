from constants import OrderStatus
from repositories import OrderRepository, UnitOfWork
from services.booking import OrderSchedulerService
from usage.order.facades import (
    DeleteOrderDomain,
    DeleteOrderDataExistenceServices
)


class OrderDeleteUsage:
    def __init__(
            self,
            order_repo: OrderRepository,
            unit_of_work: UnitOfWork,

            scheduler: OrderSchedulerService,
            domain: DeleteOrderDomain,
            data_existence: DeleteOrderDataExistenceServices,
    ) -> None:
        self._order_repo = order_repo
        self._uow = unit_of_work

        self._scheduler = scheduler
        self._domain = domain
        self._data_existence = data_existence

    async def __call__(self, order_id: int) -> None:
        order = self._data_existence.order.ensure_obj_exist(
            obj_id=order_id,
            obj=await self._order_repo.get_by_id(order_id)
        )
        self._domain.order_is_safe_to_delete(order_status=order.status)

        async with self._uow:
            await self._order_repo.delete(obj_id=order.id)

            conditions = (
                order.status == OrderStatus.PENDING,
                order.expire_schedule_id
            )

            if all(conditions):
                await self._scheduler.cancel_task(schedule_id=order.expire_schedule_id)  # type: ignore[arg-type]
