from constants import PostgresErrorCode
from exceptions.db import UniqueException, RelatedObjectNotFoundException, UniqueFieldException, \
    DeleteConstraintException
from integrity_handlers.base import TableErrorHandler
from schemas.db import ConstraintRule

uq_seats_hall_id_row_label_column_label = ConstraintRule(
    name="uq_seats_hall_id_row_label_column_label",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueException(
        "seats",
        "hall_id",
        "row_label",
        "column_label"
    )
)

fk_seats_hall_id_halls = ConstraintRule(
    name="fk_seats_hall_id_halls",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="hall_id",
        table_name="seats"
    )
)

pk_seats = ConstraintRule(
    name="pk_seats",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="id",
        table_name="seats"
    )
)

fk_tickets_seat_id_seats = ConstraintRule(
    name="fk_tickets_seat_id_seats",
    error_code=PostgresErrorCode.RESTRICT_VIOLATION,
    exception=DeleteConstraintException(
        table_name="seats",
        referencing_table="tickets"
    )
)

seat_error_handler = TableErrorHandler(
    uq_seats_hall_id_row_label_column_label,
    fk_seats_hall_id_halls,
    pk_seats,
    fk_tickets_seat_id_seats
)
