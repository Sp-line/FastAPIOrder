from repositories import (
    HallRepository,
    UnitOfWork
)
from schemas.hall import (
    HallRead,
    HallCreateReq,
    HallUpdateReq,
    HallCreateDB,
    HallUpdateDB
)
from services import ServiceBase


class HallService(
    ServiceBase[
        HallRepository,
        HallRead,
        HallCreateReq,
        HallUpdateReq,
        HallCreateDB,
        HallUpdateDB,
    ],
):
    def __init__(self, repository: HallRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="halls",
            read_schema=HallRead,
            db_create_schema=HallCreateDB,
            db_update_schema=HallUpdateDB,
        )
