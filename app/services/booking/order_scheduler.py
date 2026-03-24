from datetime import datetime

from core import redis_source
from tasks.order import set_unpaid_order_as_expired


class OrderSchedulerService:
    @staticmethod
    async def schedule_expiration(
            schedule_id: str,
            expires_at: datetime,
            order_id: int
    ) -> None:
        await (
            set_unpaid_order_as_expired
            .kicker()
            .with_schedule_id(schedule_id)
            .schedule_by_time(
                # type: ignore[call-arg]
                redis_source,
                expires_at,
                order_id=order_id,
            )
        )

    @staticmethod
    async def cancel_task(schedule_id: str) -> None:
        await redis_source.delete_schedule(schedule_id)
