from constants import PostgresErrorCode
from exceptions.db import UniqueFieldException, RelatedObjectNotFoundException
from integrity_handlers.base import TableErrorHandler
from schemas.db import ConstraintRule

uq_orders_number = ConstraintRule(
    name="uq_orders_number",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="number",
        table_name="orders"
    )
)

uq_orders_public_code = ConstraintRule(
    name="uq_orders_public_code",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="public_code",
        table_name="orders"
    )
)

uq_orders_expire_schedule_id = ConstraintRule(
    name="uq_orders_expire_schedule_id",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="expire_schedule_id",
        table_name="orders"
    )
)

fk_orders_user_id_users = ConstraintRule(
    name="fk_orders_user_id_users",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="user_id",
        table_name="orders"
    )
)

order_error_handler = TableErrorHandler(
    uq_orders_number,
    uq_orders_public_code,
    uq_orders_expire_schedule_id,
    fk_orders_user_id_users
)
