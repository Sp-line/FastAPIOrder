from core.models import Seat
from repositories.seat import SeatRepository
from repositories.unit_of_work import UnitOfWork
from schemas.seat import SeatRead, SeatCreateReq, SeatCreateDB, SeatUpdateReq, SeatUpdateDB
from services.base import ServiceBase
from services.data_existence import DataExistenceServiceBase


class SeatService(
    ServiceBase[
        SeatRepository,
        SeatRead,
        SeatCreateReq,
        SeatUpdateReq,
        SeatCreateDB,
        SeatUpdateDB,
    ],
):
    def __init__(self, repository: SeatRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="seats",
            read_schema=SeatRead,
            db_create_schema=SeatCreateDB,
            db_update_schema=SeatUpdateDB,
        )


class SeatDataExistenceService(
    DataExistenceServiceBase[
        Seat,
    ]
):
    def __init__(self) -> None:
        super().__init__(
            table_name="seats"
        )
