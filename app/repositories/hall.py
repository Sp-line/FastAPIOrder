from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Hall
from repositories import RepositoryBase
from repositories.integrity_handlers import hall_error_handler
from schemas.hall import (
    HallCreateDB,
    HallUpdateDB,
)


class HallRepository(
    RepositoryBase[
        Hall,
        HallCreateDB,
        HallUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Hall,
            session=session,
            table_error_handler=hall_error_handler,
        )
