from core.models import Session
from repositories import (
    SessionRepository,
    UnitOfWork
)
from schemas.session import (
    SessionRead,
    SessionCreateDB,
    SessionUpdateDB,
    SessionCreateReq,
    SessionUpdateReq
)
from services import (
    ServiceBase,
    DataExistenceServiceBase
)


class SessionService(
    ServiceBase[
        SessionRepository,
        SessionRead,
        SessionCreateReq,
        SessionUpdateReq,
        SessionCreateDB,
        SessionUpdateDB,
    ],
):
    def __init__(self, repository: SessionRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="sessions",
            read_schema=SessionRead,
            db_create_schema=SessionCreateDB,
            db_update_schema=SessionUpdateDB,
        )


class SessionDataExistenceService(
    DataExistenceServiceBase[
        Session,
    ]
):
    def __init__(self) -> None:
        super().__init__(
            table_name="sessions"
        )
