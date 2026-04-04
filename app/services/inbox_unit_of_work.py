from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from uuid import UUID

from repositories import UnitOfWork, InboxEventCommandRepository
from schemas.inbox_events import InboxEventCreateDB

type ShouldProceed = bool


class InboxUnitOfWork:
    def __init__(
            self,
            uow: UnitOfWork,
            repo: InboxEventCommandRepository
    ):
        self.uow = uow
        self.repo = repo

    @asynccontextmanager
    async def transactional(self, msg_id: UUID | None) -> AsyncIterator[ShouldProceed]:
        if msg_id is None:
            raise ValueError("Nats-Msg-Id is required for deduplication")

        async with self.uow:
            is_new = await self.repo.add_if_not_exists(
                InboxEventCreateDB(code=msg_id)
            )

            if not is_new:
                yield False
                return

            yield True
