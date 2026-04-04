from constants import PostgresErrorCode
from exceptions.db import UniqueFieldException
from repositories.integrity_handlers import TableErrorHandler
from schemas.db import ConstraintRule

uq_inbox_events_code = ConstraintRule(
    name="uq_inbox_events_code",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="code",
        table_name="inbox_events"
    )
)

pk_inbox_events = ConstraintRule(
    name="pk_inbox_events",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="id",
        table_name="inbox_events"
    )
)

inbox_events_error_handler = TableErrorHandler(
    uq_inbox_events_code,
    pk_inbox_events,
)
