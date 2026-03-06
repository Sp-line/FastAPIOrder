from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from constants import OrderStatus
from core.models import Order
from integrity_handlers.order import order_error_handler
from repositories.base import RepositoryBase
from schemas.order import OrderCreateDB, OrderUpdateDB


class OrderRepository(
    RepositoryBase[
        Order,
        OrderCreateDB,
        OrderUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Order,
            session=session,
            table_error_handler=order_error_handler,
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
