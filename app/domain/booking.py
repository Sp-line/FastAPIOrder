from datetime import datetime, timedelta

from constants import OrderStatus
from exceptions.business import BusinessLogicException


class BookingDomain:
    @staticmethod
    def ensure_order_can_be_modified(order_status: OrderStatus) -> None:
        if order_status != OrderStatus.PENDING:
            raise BusinessLogicException(
                message="Cannot change an order unless it is in the pending status."
            )

    @staticmethod
    def ensure_session_is_open(now: datetime, start_time: datetime, buffer_minutes: int) -> None:
        cutoff_time = start_time + timedelta(minutes=buffer_minutes)
        if now > cutoff_time:
            raise BusinessLogicException(
                message="Ticket sales for this session are already closed."
            )


    @staticmethod
    def ensure_seat_valid_for_session(seat_hall_id: int, session_hall_id: int) -> None:
        if seat_hall_id != session_hall_id:
            raise BusinessLogicException(
                message="The selected seat does not belong to the session's hall."
            )

    @staticmethod
    def ensure_user_can_create_order(has_active_orders: bool) -> None:
        if has_active_orders:
            raise BusinessLogicException(
                message="You already have an active unpaid order."
            )
