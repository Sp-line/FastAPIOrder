from constants.db import PostgresErrorCode
from exceptions.db import UniqueFieldException, DeleteConstraintException
from repositories.integrity_handlers.base import TableErrorHandler
from schemas.db import ConstraintRule

uq_halls_slug = ConstraintRule(
    name="uq_halls_slug",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="slug",
        table_name="halls"
    )
)

fk_sessions_hall_id_halls_delete = ConstraintRule(
    name="fk_sessions_hall_id_halls",
    error_code=PostgresErrorCode.RESTRICT_VIOLATION,
    exception=DeleteConstraintException(
        table_name="halls",
        referencing_table="sessions"
    )
)

pk_halls = ConstraintRule(
    name="pk_halls",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="id",
        table_name="halls"
    )
)

hall_error_handler = TableErrorHandler(
    uq_halls_slug,
    fk_sessions_hall_id_halls_delete,
    pk_halls
)
