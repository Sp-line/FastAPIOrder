from uuid import UUID

from core.models import Ticket
from exceptions.db import ObjectNotFoundException
from repositories.ticket import TicketQueryRepository
from schemas.ticket import TicketRead
from services import (
    QueryServiceBase,
    DataExistenceServiceBase
)


class TicketQueryService(
    QueryServiceBase[
        TicketQueryRepository,
        TicketRead
    ]
):
    def __init__(self, repository: TicketQueryRepository) -> None:
        super().__init__(
            repository=repository,
            table_name="tickets",
            read_schema=TicketRead,
        )

    async def get_by_public_code(self, public_code: UUID) -> TicketRead:
        if not (obj := await self._repository.get_by_public_code(public_code)):
            raise ObjectNotFoundException(
                conditions={
                    "public_code": public_code,
                },
                table_name=self._table_name
            )
        return self._read_schema.model_validate(obj)

    async def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> list[TicketRead]:
        objs = await self._repository.get_by_user_id(user_id=user_id, skip=skip, limit=limit)
        return [self._read_schema.model_validate(ticket) for ticket in objs]


class TicketDataExistenceService(
    DataExistenceServiceBase[
        Ticket,
    ]
):
    def __init__(self) -> None:
        super().__init__(
            table_name="tickets"
        )
