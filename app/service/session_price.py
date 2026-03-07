from repositories.session_price import SessionPriceRepository
from repositories.unit_of_work import UnitOfWork
from schemas.session_price import SessionPriceRead, SessionPriceCreateReq, SessionPriceUpdateReq, SessionPriceCreateDB, \
    SessionPriceUpdateDB
from service.base import ServiceBase


class SessionPriceService(
    ServiceBase[
        SessionPriceRepository,
        SessionPriceRead,
        SessionPriceCreateReq,
        SessionPriceUpdateReq,
        SessionPriceCreateDB,
        SessionPriceUpdateDB,
    ],
):
    def __init__(self, repository: SessionPriceRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="seats",
            read_schema=SessionPriceRead,
            db_create_schema=SessionPriceCreateDB,
            db_update_schema=SessionPriceUpdateDB,
        )
