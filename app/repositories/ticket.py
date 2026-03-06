from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Ticket
from integrity_handlers.ticket import ticket_error_handler
from repositories.base import RepositoryBase
from schemas.ticket import TicketUpdateDB, TicketCreateDB


class TicketRepository(
    RepositoryBase[
        Ticket,
        TicketCreateDB,
        TicketUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Ticket,
            session=session,
            table_error_handler=ticket_error_handler,
        )

