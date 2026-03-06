from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Movie
from integrity_handlers.movie import movie_error_handler
from repositories.base import RepositoryBase
from schemas.movie import MovieCreateDB, MovieUpdateDB


class MovieRepository(
    RepositoryBase[
        Movie,
        MovieCreateDB,
        MovieUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Movie,
            session=session,
            table_error_handler=movie_error_handler,
        )