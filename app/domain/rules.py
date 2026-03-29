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
            TicketStatus.RESERVED: {TicketStatus.PAID, TicketStatus.CANCELLED, TicketStatus.EXPIRED},
            TicketStatus.PAID: {TicketStatus.USED, TicketStatus.REFUND_PENDING},
            TicketStatus.USED: {TicketStatus.REFUND_PENDING},
            TicketStatus.REFUND_PENDING: {TicketStatus.REFUNDED, TicketStatus.PAID},

            TicketStatus.EXPIRED: set(),
            TicketStatus.REFUNDED: set(),
            TicketStatus.CANCELLED: set(),
        }

        if target_status not in allowed_transitions.get(current_status, set()):
            raise BusinessLogicException(
                message=f"Invalid ticket status transition from '{current_status.value}' to '{target_status.value}'."
            )


class EnsureValidOrderStatusTransition:
    def __call__(self, current_status: OrderStatus, target_status: OrderStatus) -> None:
        if current_status == target_status:
            raise BusinessLogicException(f"Order is already in '{target_status.value}' status.")

        allowed_transitions = {
            OrderStatus.PENDING: {OrderStatus.PAID, OrderStatus.CANCELED, OrderStatus.EXPIRED},
            OrderStatus.PAID: {OrderStatus.REFUND_PENDING, OrderStatus.REFUNDED},
            OrderStatus.REFUND_PENDING: {OrderStatus.REFUNDED, OrderStatus.CANCELED},

            OrderStatus.EXPIRED: set(),
            OrderStatus.FAILED: set(),
            OrderStatus.CANCELED: set(),
            OrderStatus.REFUNDED: set(),
        }

        if target_status not in allowed_transitions.get(current_status, set()):
            raise BusinessLogicException(
                f"Invalid order status transition from '{current_status.value}' to '{target_status.value}'."
            )


class EnsureOrderIsPendingForPriceChange:
    def __call__(self, order_status: OrderStatus) -> None:
        if order_status != OrderStatus.PENDING:
            raise BusinessLogicException(
                message="Cannot change ticket price. Order must be in PENDING status."
            )


class EnsureTicketIsReservedForPriceChange:
    def __call__(self, ticket_status: TicketStatus) -> None:
        if ticket_status != TicketStatus.RESERVED:
            raise BusinessLogicException(
                message=f"Cannot change ticket price. Ticket must be in RESERVED status."
            )


class EnsureOrderIsSafeToDelete:
    def __call__(self, order_status: OrderStatus) -> None:
        unsafe_statuses = {OrderStatus.PAID, OrderStatus.REFUND_PENDING}

        if order_status in unsafe_statuses:
            raise BusinessLogicException(
                message=f"Cannot hard-delete order in '{order_status.value}' status. "
                        "Please process a refund and change status to CANCELLED or REFUNDED first."
            )


class SyncOrderStatusWithTickets:
    def __call__(self, order_status: OrderStatus, ticket_statuses: set[TicketStatus]) -> OrderStatus | None:
        if not ticket_statuses:
            return None

        new_status = None

        if ticket_statuses == {TicketStatus.CANCELLED}:
            new_status = OrderStatus.CANCELED
        elif ticket_statuses == {TicketStatus.EXPIRED}:
            new_status = OrderStatus.EXPIRED
        elif ticket_statuses == {TicketStatus.REFUNDED}:
            new_status = OrderStatus.REFUNDED

        if new_status and new_status != order_status:
            return new_status

        return None
