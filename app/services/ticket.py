from core.models import Ticket
from repositories.ticket import TicketQueryRepository
from schemas.ticket import TicketAdminRead
from services import (
    QueryServiceBase,
    DataExistenceServiceBase
)


class TicketQueryService(
    QueryServiceBase[
        TicketQueryRepository,
        TicketAdminRead
    ]
):
    def __init__(self, repository: TicketQueryRepository) -> None:
        super().__init__(
            repository=repository,
            table_name="tickets",
            read_schema=TicketAdminRead,
        )


class TicketDataExistenceService(
    DataExistenceServiceBase[
        Ticket,
    ]
):
    def __init__(self) -> None:
        super().__init__(
            table_name="tickets"
        )
