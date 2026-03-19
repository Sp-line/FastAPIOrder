from constants import PostgresErrorCode
from exceptions.db import DeleteConstraintException, UniqueFieldException
from repositories.integrity_handlers.base import TableErrorHandler
from schemas.db import ConstraintRule

uq_movies_slug = ConstraintRule(
    name="uq_movies_slug",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="slug",
        table_name="movies"
    )
)

pk_movies = ConstraintRule(
    name="pk_movies",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="id",
        table_name="movies"
    )
)

fk_sessions_movie_id_movies = ConstraintRule(
    name="fk_sessions_movie_id_movies",
    error_code=PostgresErrorCode.RESTRICT_VIOLATION,
    exception=DeleteConstraintException(
        table_name="movies",
        referencing_table="sessions"
    )
)

movie_error_handler = TableErrorHandler(
    uq_movies_slug,
    pk_movies,
    fk_sessions_movie_id_movies
)