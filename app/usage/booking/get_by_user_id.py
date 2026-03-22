from pydantic import TypeAdapter

from repositories.order import OrderQueryRepository
from schemas.booking import BookingOrderRead


class GetBookingsByUserIDUsage:
    def __init__(
            self,
            order_query_repo: OrderQueryRepository,
    ) -> None:
        self._order_query_repo = order_query_repo

    async def __call__(self, user_id: int, skip: int = 0, limit: int = 100) -> list[BookingOrderRead]:
        adapter = TypeAdapter(list[BookingOrderRead])
        objs = await self._order_query_repo.get_aggregates_by_user_id(user_id, skip, limit)
        return adapter.validate_python(objs)
