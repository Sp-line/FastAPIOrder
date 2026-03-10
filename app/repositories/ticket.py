from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Ticket
from integrity_handlers.ticket import ticket_error_handler
from repositories.base import QueryRepositoryBase, CommandRepositoryBase
from schemas.ticket import TicketUpdateDB, TicketCreateDB


class TicketQueryRepository(
    QueryRepositoryBase[
        Ticket,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Ticket,
            session=session
        )

    async def get_by_public_code(self, public_code: UUID) -> Ticket | None:
        stmt = (
            select(self._model)
            .where(self._model.public_code == public_code)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()


class TicketCommandRepository(
    CommandRepositoryBase[
        Ticket,
        TicketCreateDB,
        TicketUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Ticket,
            session=session,
            table_error_handler=ticket_error_handler
        )
