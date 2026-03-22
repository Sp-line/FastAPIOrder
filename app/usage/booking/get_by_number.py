from uuid import UUID

from exceptions.db import ObjectNotFoundException
from repositories.order import OrderQueryRepository
from schemas.booking import BookingOrderRead


class GetBookingByNumberUsage:
    def __init__(
            self,
            order_query_repo: OrderQueryRepository,
    ) -> None:
        self._order_query_repo = order_query_repo

    async def __call__(self, order_number: UUID) -> BookingOrderRead:
        if not (obj := await self._order_query_repo.get_aggregate_by_number(order_number)):
            raise ObjectNotFoundException(
                conditions={
                    "order_number": order_number,
                },
                table_name="orders"
            )
        return BookingOrderRead.model_validate(obj)
