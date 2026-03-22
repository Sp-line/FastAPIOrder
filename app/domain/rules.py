from datetime import datetime, timezone, timedelta

from constants import OrderStatus, OrderLimits
from exceptions.business import BusinessLogicException


class EnsureOrderCanBeModified:
    def __call__(self, order_status: OrderStatus) -> None:
        if order_status != OrderStatus.PENDING:
            raise BusinessLogicException(
                message="Cannot change an order unless it is in the pending status."
            )


class EnsureSessionIsOpen:
    def __init__(self, buffer_minutes: int = OrderLimits.BUFFER_TIME_MINUTES) -> None:
        self._buffer_minutes = buffer_minutes

    def __call__(self, start_time: datetime) -> None:
        now = datetime.now(timezone.utc)
        cutoff_time = start_time + timedelta(minutes=self._buffer_minutes)
        if now > cutoff_time:
            raise BusinessLogicException(
                message="Ticket sales for this session are already closed."
            )


class EnsureSeatValidForSession:
    def __call__(self, seat_hall_id: int, session_hall_id: int) -> None:
        if seat_hall_id != session_hall_id:
            raise BusinessLogicException(
                message="The selected seat does not belong to the session's hall."
            )


class EnsureUserCanCreateOrder:
    def __call__(self, has_active_orders: bool) -> None:
        if has_active_orders:
            raise BusinessLogicException(
                message="You already have an active unpaid order."
            )
