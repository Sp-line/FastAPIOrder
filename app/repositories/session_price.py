from decimal import Decimal
from typing import Sequence, Iterable

from sqlalchemy import select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession

from constants import SeatType
from core.models import SessionPrice
from integrity_handlers.session_price import session_price_error_handler
from repositories.base import RepositoryBase
from schemas.session_price import SessionPriceCreateDB, SessionPriceUpdateDB, SessionPriceCombination


class SessionPriceRepository(
    RepositoryBase[
        SessionPrice,
        SessionPriceCreateDB,
        SessionPriceUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=SessionPrice,
            session=session,
            table_error_handler=session_price_error_handler,
        )

    async def get_price_for_seat_type(self, session_id: int, seat_type: SeatType) -> Decimal | None:
        stmt = select(SessionPrice.price).where(
            SessionPrice.session_id == session_id,
            SessionPrice.seat_type == seat_type
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_prices_by_session_and_seat_types(
            self,
            combinations: Iterable[SessionPriceCombination]
    ) -> Sequence[SessionPrice]:
        tuple_filters = [(c.session_id, c.seat_type) for c in combinations]

        if not tuple_filters:
            return []

        stmt = (
            select(SessionPrice)
            .where(
                tuple_(SessionPrice.session_id, SessionPrice.seat_type).in_(tuple_filters)
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
