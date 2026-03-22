from core.models import Order
from repositories.order import OrderQueryRepository
from schemas.order import OrderAdminRead
from services.base import QueryServiceBase
from services.data_existence import DataExistenceServiceBase


class OrderQueryService(
    QueryServiceBase[
        OrderQueryRepository,
        OrderAdminRead
    ]
):
    def __init__(self, repository: OrderQueryRepository) -> None:
        super().__init__(
            repository=repository,
            table_name="orders",
            read_schema=OrderAdminRead,
        )


class OrderDataExistenceService(
    DataExistenceServiceBase[
        Order,
    ]
):
    def __init__(self) -> None:
        super().__init__(
            table_name="orders"
        )
