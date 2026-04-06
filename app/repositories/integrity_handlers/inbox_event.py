from constants import PostgresErrorCode
from exceptions.db import UniqueFieldException, UniqueException
from repositories.integrity_handlers import TableErrorHandler
from schemas.db import ConstraintRule

uq_inbox_events_code_handler = ConstraintRule(
    name="uq_inbox_events_code_handler",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueException(
        "inbox_events",
        "code", "handler"
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
    uq_inbox_events_code_handler,
    pk_inbox_events,
)
