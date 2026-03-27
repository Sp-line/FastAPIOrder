from constants import PostgresErrorCode
from exceptions.db import (
    UniqueFieldException,
    RelatedObjectNotFoundException,
    UniqueException,
)
from repositories.integrity_handlers.base import TableErrorHandler
from schemas.db import ConstraintRule

uq_tickets_public_code = ConstraintRule(
    name="uq_tickets_public_code",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="public_code",
        table_name="tickets"
    )
)

fk_tickets_order_id_orders = ConstraintRule(
    name="fk_tickets_order_id_orders",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="order_id",
        table_name="tickets"
    )
)

fk_tickets_session_id_sessions = ConstraintRule(
    name="fk_tickets_session_id_sessions",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="session_id",
        table_name="tickets"
    )
)

fk_tickets_seat_id_seats = ConstraintRule(
    name="fk_tickets_seat_id_seats",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="seat_id",
        table_name="tickets"
    )
)

ix_unique_active_ticket_per_seat = ConstraintRule(
    name="ix_unique_active_ticket_per_seat",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueException(
        "tickets",
        "session_id", "seat_id"
    )
)

pk_tickets = ConstraintRule(
    name="pk_tickets",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="id",
        table_name="tickets"
    )
)

ticket_error_handler = TableErrorHandler(
    uq_tickets_public_code,
    fk_tickets_order_id_orders,
    fk_tickets_session_id_sessions,
    fk_tickets_seat_id_seats,
    ix_unique_active_ticket_per_seat,
    pk_tickets
)
