from constants import OrderStatus
from core import broker
from repositories.order import OrderRepository
from repositories.unit_of_work import UnitOfWork
from dishka.integrations.taskiq import FromDishka, inject

from schemas.order import OrderUpdateDB


@broker.task
@inject(patch_module=True)
async def set_unpaid_order_as_expired(
        order_repository: FromDishka[OrderRepository],
        uof: FromDishka[UnitOfWork],
        order_id: int
) -> None:
    async with uof:
        order = await order_repository.get_by_id(order_id)
        if not order:
            return

        if order.status == OrderStatus.PENDING:
            await order_repository.update(
                order.id,
                OrderUpdateDB(
                    status=OrderStatus.EXPIRED,
                )
            )
