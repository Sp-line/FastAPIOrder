from collections.abc import Iterable
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import Seat
from repositories import RepositoryBase
from repositories.integrity_handlers import seat_error_handler
from schemas.seat import (
    SeatCreateDB,
    SeatUpdateDB
)


class SeatRepository(
    RepositoryBase[
        Seat,
        SeatCreateDB,
        SeatUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Seat,
            session=session,
            table_error_handler=seat_error_handler,
        )

    async def get_with_hall(self, seat_id: int) -> Seat | None:
        stmt = (
            select(Seat)
            .options(joinedload(Seat.hall))
            .where(Seat.id == seat_id)
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_many_with_hall(self, hall_ids: Iterable[int]) -> Sequence[Seat]:
        if not hall_ids:
            return []

        stmt = (
            select(Seat)
            .where(Seat.id.in_(hall_ids))
            .options(joinedload(Seat.hall))
        )

        result = await self._session.execute(stmt)
        return result.scalars().all()
