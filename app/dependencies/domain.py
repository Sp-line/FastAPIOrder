from dishka import (
    Provider,
    Scope,
    provide
)

from domain import (
    EnsureOrderCanBeModified,
    EnsureSessionIsOpen,
    EnsureSeatValidForSession,
    EnsureUserCanCreateOrder,
    EnsureValidTicketStatusTransition,
    EnsureOrderIsPendingForPriceChange,
    EnsureTicketIsReservedForPriceChange,
    EnsureValidOrderStatusTransition,
    EnsureOrderIsSafeToDelete,
)
from usage.booking.facades import CreateBookingDomain
from usage.order.facades import (
    DeleteOrderDomain,
    UpdateOrderStatusDomain
)
from usage.ticket.facades import (
    AddTicketToOrderDomain,
    AddTicketsToOrdersDomain,
    RemoveTicketFromOrderDomain,
    UpdateTicketPriceInOrderDomain,
    UpdateTicketStatusInOrderDomain
)


class DomainProvider(Provider):
    scope = Scope.APP

    get_ensure_order_can_be_modified = provide(EnsureOrderCanBeModified)
    get_ensure_seat_valid_for_session = provide(EnsureSeatValidForSession)
    get_ensure_user_can_create_order = provide(EnsureUserCanCreateOrder)
    get_ensure_valid_ticket_status_transition = provide(EnsureValidTicketStatusTransition)
    get_ensure_order_is_pending_for_price_change = provide(EnsureOrderIsPendingForPriceChange)
    get_ensure_ticket_is_reserved_for_price_change = provide(EnsureTicketIsReservedForPriceChange)
    get_ensure_valid_order_status_transition = provide(EnsureValidOrderStatusTransition)
    get_ensure_order_is_safe_to_delete = provide(EnsureOrderIsSafeToDelete)

    @provide
    def get_ensure_session_is_open(self) -> EnsureSessionIsOpen:
        return EnsureSessionIsOpen()

    get_create_booking_domain = provide(CreateBookingDomain)

    get_add_ticket_to_order_domain = provide(AddTicketToOrderDomain)
    get_add_tickets_to_orders_domain = provide(AddTicketsToOrdersDomain)
    get_remove_ticket_from_order_domain = provide(RemoveTicketFromOrderDomain)
    get_update_ticket_status_in_order_domain = provide(UpdateTicketStatusInOrderDomain)
    get_update_ticket_price_in_order_domain = provide(UpdateTicketPriceInOrderDomain)

    get_update_order_status_domain = provide(UpdateOrderStatusDomain)
    get_delete_order_domain = provide(DeleteOrderDomain)
