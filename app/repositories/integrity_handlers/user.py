from constants import PostgresErrorCode
from exceptions.db import UniqueFieldException, DeleteConstraintException
from repositories.integrity_handlers.base import TableErrorHandler
from schemas.db import ConstraintRule

pk_users = ConstraintRule(
    name="pk_users",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="id",
        table_name="users"
    )
)

uq_users_email = ConstraintRule(
    name="uq_users_email",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="email",
        table_name="users"
    )
)

uq_users_phone_number = ConstraintRule(
    name="uq_users_phone_number",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueFieldException(
        field_name="phone_number",
        table_name="users"
    )
)

fk_orders_user_id_users = ConstraintRule(
    name="fk_orders_user_id_users",
    error_code=PostgresErrorCode.RESTRICT_VIOLATION,
    exception=DeleteConstraintException(
        table_name="users",
        referencing_table="orders"
    )
)

user_error_handler = TableErrorHandler(
    pk_users,
    uq_users_email,
    uq_users_phone_number,
    fk_orders_user_id_users
)
