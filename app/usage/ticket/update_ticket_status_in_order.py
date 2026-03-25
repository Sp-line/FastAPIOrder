from constants import OrderStatus
from repositories import (
    TicketRepository,
    UnitOfWork,
    OrderRepository
)
from schemas.order import OrderUpdateDB
from schemas.ticket import (
    TicketStatusUpdateReq,
    TicketRead,
    TicketUpdateDB
)
from services import TaskScheduler
from usage.ticket.facades import (
    UpdateTicketStatusInOrderDomain,
    UpdateTicketStatusInOrderDataExistenceServices
)


class UpdateTicketStatusInOrderUsage:
    def __init__(
            self,
            ticket_repo: TicketRepository,
            order_repo: OrderRepository,
            unit_of_work: UnitOfWork,

            scheduler: TaskScheduler,
            domain: UpdateTicketStatusInOrderDomain,
            data_existence: UpdateTicketStatusInOrderDataExistenceServices
    ) -> None:
        self._ticket_repo = ticket_repo
        self._order_repo = order_repo
        self._uow = unit_of_work

        self._domain = domain
        self._scheduler = scheduler
        self._data_existence = data_existence

    async def __call__(self, ticket_id: int, data: TicketStatusUpdateReq) -> TicketRead:
        ticket = self._data_existence.ticket.ensure_obj_exist(
            obj_id=ticket_id,
            obj=await self._ticket_repo.get_by_id(ticket_id)
        )

        self._domain.valid_ticket_status_transition(
            current_status=ticket.status,
            target_status=data.status
        )

        async with self._uow:
            updated_ticket_db = await self._ticket_repo.update(
                obj_id=ticket.id,
                data=TicketUpdateDB(status=data.status)
            )
            updated_ticket = self._data_existence.ticket.ensure_obj_exist(
                obj_id=ticket_id,
                obj=updated_ticket_db
            )

            not_updated_order = self._data_existence.order.ensure_obj_exist(
                obj_id=updated_ticket.order_id,
                obj=await self._order_repo.get_with_tickets(updated_ticket.order_id)
            )

            if not_updated_order.tickets:
                ticket_statuses = {ticket.status for ticket in not_updated_order.tickets}

                new_order_status = self._domain.sync_order_status_with_tickets(
                    order_status=not_updated_order.status,
                    ticket_statuses=ticket_statuses
                )

                if new_order_status:
                    await self._order_repo.update(
                        obj_id=not_updated_order.id,
                        data=OrderUpdateDB(status=new_order_status)
                    )

                    conditions = (
                        not_updated_order.status == OrderStatus.PENDING,
                        not_updated_order.expire_schedule_id
                    )

                    if all(conditions):
                        await self._scheduler.cancel_schedule(
                            schedule_id=not_updated_order.expire_schedule_id  # type: ignore[arg-type]
                        )

            return TicketRead.model_validate(updated_ticket)
