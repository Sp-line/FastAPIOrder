from collections.abc import Iterable
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import Session
from repositories import RepositoryBase
from repositories.integrity_handlers import session_error_handler
from schemas.session import (
    SessionCreateDB,
    SessionUpdateDB
)


class SessionRepository(
    RepositoryBase[
        Session,
        SessionCreateDB,
        SessionUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Session,
            session=session,
            table_error_handler=session_error_handler,
        )

    async def get_with_movie(self, session_id: int) -> Session | None:
        stmt = (
            select(Session)
            .options(joinedload(Session.movie))
            .where(Session.id == session_id)
        )
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_many_with_movie(self, session_ids: Iterable[int]) -> Sequence[Session]:
        if not session_ids:
            return []

        stmt = (
            select(Session)
            .where(Session.id.in_(session_ids))
            .options(joinedload(Session.movie))
        )

        result = await self._session.execute(stmt)
        return result.scalars().all()
