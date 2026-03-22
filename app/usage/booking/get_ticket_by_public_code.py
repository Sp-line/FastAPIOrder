from uuid import UUID

from repositories import TicketRepository
from schemas.ticket import TicketRead
from services import TicketDataExistenceService


class GetTicketByPublicCodeUsage:
    def __init__(
            self,
            ticket_repo: TicketRepository,
            ticket_data_existence: TicketDataExistenceService,
    ) -> None:
        self._ticket_repo = ticket_repo
        self._ticket_data_existence = ticket_data_existence

    async def __call__(self, public_code: UUID) -> TicketRead:
        ticket = self._ticket_data_existence.ensure_obj_exist(
            obj=await self._ticket_repo.get_by_public_code(public_code),
            conditions={
                "public_code": public_code,
            },
        )
        return TicketRead.model_validate(ticket)
