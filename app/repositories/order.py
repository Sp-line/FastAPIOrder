from datetime import (
    datetime,
    timezone
)
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from constants import OrderStatus
from core.models import Order
from repositories import (
    QueryRepositoryBase,
    CommandRepositoryBase
)
from repositories.integrity_handlers import order_error_handler
from schemas.order import (
    OrderCreateDB,
    OrderUpdateDB
)


class OrderQueryRepository(
    QueryRepositoryBase[
        Order,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Order,
            session=session
        )

    async def has_active_unpaid_order(self, user_id: int) -> bool:
        stmt = (
            select(self._model.id)
            .where(
                self._model.user_id == user_id,
                self._model.status == OrderStatus.PENDING,
                self._model.expires_at > datetime.now(timezone.utc)
            )
            .limit(1)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_aggregate_by_number(self, order_number: UUID) -> Order | None:
        stmt = (
            select(self._model)
            .where(self._model.number == order_number)
            .options(
                selectinload(self._model.tickets)
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_aggregates_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> Sequence[Order]:
        stmt = (
            select(self._model)
            .where(self._model.user_id == user_id)
            .options(
                selectinload(self._model.tickets)
            )
            .offset(skip)
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_with_tickets(self, order_id: int) -> Order | None:
        stmt = (
            select(self._model)
            .where(self._model.id == order_id)
            .options(selectinload(self._model.tickets))
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()


class OrderCommandRepository(
    CommandRepositoryBase[
        Order,
        OrderCreateDB,
        OrderUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Order,
            session=session,
            table_error_handler=order_error_handler
        )


class OrderRepository(
    OrderQueryRepository,
    OrderCommandRepository
):
    def __init__(self, session: AsyncSession) -> None:
        OrderQueryRepository.__init__(self, session=session)
        OrderCommandRepository.__init__(self, session=session)
