from datetime import (
    datetime,
    timezone,
    timedelta
)

from constants import (
    OrderStatus,
    OrderLimits,
    TicketStatus
)
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


class EnsureValidTicketStatusTransition:
    def __call__(self, current_status: TicketStatus, target_status: TicketStatus) -> None:
        if current_status == target_status:
            raise BusinessLogicException(
                message=f"Ticket is already in '{target_status.value}' status."
            )

        allowed_transitions = {
            TicketStatus.RESERVED: {TicketStatus.ACTIVE, TicketStatus.CANCELLED},
            TicketStatus.ACTIVE: {TicketStatus.USED, TicketStatus.REFUND_PENDING, TicketStatus.CANCELLED},
            TicketStatus.USED: {TicketStatus.ACTIVE, TicketStatus.REFUND_PENDING},
            TicketStatus.EXPIRED: set(),
            TicketStatus.REFUNDED: set(),
            TicketStatus.REFUND_PENDING: set(),
            TicketStatus.CANCELLED: set(),
        }

        if target_status not in allowed_transitions.get(current_status, set()):
            raise BusinessLogicException(
                message=f"Invalid ticket status transition from '{current_status.value}' to '{target_status.value}'."
            )
