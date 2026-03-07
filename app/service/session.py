from repositories.session import SessionRepository
from repositories.unit_of_work import UnitOfWork
from schemas.session import SessionRead, SessionCreateDB, SessionUpdateDB, SessionCreateReq, SessionUpdateReq
from service.base import ServiceBase


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
            table_name="seats",
            read_schema=SessionRead,
            db_create_schema=SessionCreateDB,
            db_update_schema=SessionUpdateDB,
        )
