from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Ticket, Order
from repositories.integrity_handlers import ticket_error_handler
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

    async def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> Sequence[Ticket]:
        stmt = (
            select(self._model)
            .join(Order, self._model.order_id == Order.id)
            .where(Order.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        return result.scalars().all()


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


class TicketRepository(
    TicketQueryRepository,
    TicketCommandRepository
):
    def __init__(self, session: AsyncSession) -> None:
        TicketQueryRepository.__init__(self, session=session)
        TicketCommandRepository.__init__(self, session=session)
