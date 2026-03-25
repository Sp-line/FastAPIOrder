from dishka.integrations.taskiq import (
    FromDishka,
    inject
)

from constants import OrderStatus, TicketStatus
from core import broker
from repositories import (
    OrderRepository,
    UnitOfWork,
    TicketRepository
)
from schemas.order import OrderUpdateDB
from schemas.ticket import TicketUpdateDB


@broker.task
@inject(patch_module=True)
async def set_unpaid_order_with_tickets_as_expired(
        order_repo: FromDishka[OrderRepository],
        ticket_repo: FromDishka[TicketRepository],
        uof: FromDishka[UnitOfWork],
        order_id: int
) -> None:
    async with uof:
        order = await order_repo.get_with_tickets(order_id)
        if not order:
            return

        if order.status == OrderStatus.PENDING:
            await order_repo.update(
                order.id,
                OrderUpdateDB(
                    status=OrderStatus.EXPIRED,
                )
            )

            if order.tickets:
                tickets_update_data = {
                    ticket.id: TicketUpdateDB(status=TicketStatus.EXPIRED)
                    for ticket in order.tickets
                }

                await ticket_repo.bulk_update(tickets_update_data)
