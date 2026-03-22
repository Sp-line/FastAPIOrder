from pydantic import TypeAdapter

from repositories import TicketRepository
from schemas.ticket import TicketRead
from services import TicketDataExistenceService


class GetTicketsByUserIdUsage:
    def __init__(
            self,
            ticket_repo: TicketRepository,
            ticket_data_existence: TicketDataExistenceService,
    ) -> None:
        self._ticket_repo = ticket_repo
        self._ticket_data_existence = ticket_data_existence

    async def __call__(self, user_id: int, skip: int = 0, limit: int = 100) -> list[TicketRead]:
        tickets = await self._ticket_repo.get_by_user_id(user_id=user_id, skip=skip, limit=limit)
        adapter = TypeAdapter(list[TicketRead])
        return adapter.validate_python(tickets)
