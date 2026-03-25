from repositories import (
    TicketRepository,
    UnitOfWork
)
from schemas.ticket import (
    TicketStatusUpdateReq,
    TicketRead,
    TicketUpdateDB
)
from usage.ticket.facades import (
    UpdateTicketStatusInOrderDomain,
    UpdateTicketStatusInOrderDataExistenceServices
)


class UpdateTicketStatusInOrderUsage:
    def __init__(
            self,
            ticket_repo: TicketRepository,
            unit_of_work: UnitOfWork,

            domain: UpdateTicketStatusInOrderDomain,
            data_existence: UpdateTicketStatusInOrderDataExistenceServices
    ) -> None:
        self._ticket_repo = ticket_repo
        self._uow = unit_of_work

        self._domain = domain
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
            updated_ticket = await self._ticket_repo.update(
                obj_id=ticket.id,
                data=TicketUpdateDB(status=data.status)
            )

            return TicketRead.model_validate(updated_ticket)
