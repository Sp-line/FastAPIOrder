from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper


class InfrastructureProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_db_session(self) -> AsyncIterable[AsyncSession]:
        async with db_helper.session_factory() as session:
            yield session
