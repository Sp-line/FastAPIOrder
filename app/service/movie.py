from repositories.movie import MovieRepository
from repositories.unit_of_work import UnitOfWork
from schemas.movie import MovieRead, MovieCreateReq, MovieUpdateReq, MovieCreateDB, MovieUpdateDB
from service.base import ServiceBase


class MovieService(
    ServiceBase[
        MovieRepository,
        MovieRead,
        MovieCreateReq,
        MovieUpdateReq,
        MovieCreateDB,
        MovieUpdateDB,
    ],
):
    def __init__(self, repository: MovieRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="movies",
            read_schema=MovieRead,
            db_create_schema=MovieCreateDB,
            db_update_schema=MovieUpdateDB,
        )
