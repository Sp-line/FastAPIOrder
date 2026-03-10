from repositories.ticket import TicketQueryRepository
from schemas.ticket import TicketRead
from service.base import QueryServiceBase


class TicketQueryService(
    QueryServiceBase[
        TicketQueryRepository,
        TicketRead
    ]
):
    def __init__(self, repository: TicketQueryRepository) -> None:
        super().__init__(
            repository=repository,
            table_name="tickets",
            read_schema=TicketRead,
        )
        