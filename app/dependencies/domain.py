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
)
from usage.booking.create_order import CreateBookingDomain
from usage.ticket.add_ticket_to_order import AddTicketToOrderDomain
from usage.ticket.add_tickets_to_orders import AddTicketsToOrdersDomain
from usage.ticket.remove_ticket_from_order import RemoveTicketFromOrderDomain
from usage.ticket.update_ticket_price_in_order import UpdateTicketPriceInOrderDomain
from usage.ticket.update_ticket_status_in_order import UpdateTicketStatusInOrderDomain


class DomainProvider(Provider):
    scope = Scope.APP

    get_ensure_order_can_be_modified = provide(EnsureOrderCanBeModified)
    get_ensure_seat_valid_for_session = provide(EnsureSeatValidForSession)
    get_ensure_user_can_create_order = provide(EnsureUserCanCreateOrder)
    get_ensure_valid_ticket_status_transition = provide(EnsureValidTicketStatusTransition)
    get_ensure_order_is_pending_for_price_change = provide(EnsureOrderIsPendingForPriceChange)
    get_ensure_ticket_is_reserved_for_price_change = provide(EnsureTicketIsReservedForPriceChange)

    @provide
    def get_ensure_session_is_open(self) -> EnsureSessionIsOpen:
        return EnsureSessionIsOpen()

    get_create_booking_domain = provide(CreateBookingDomain)

    get_add_ticket_to_order_domain = provide(AddTicketToOrderDomain)
    get_add_tickets_to_orders_domain = provide(AddTicketsToOrdersDomain)
    get_remove_ticket_from_order_domain = provide(RemoveTicketFromOrderDomain)
    get_update_ticket_status_in_order_domain = provide(UpdateTicketStatusInOrderDomain)
    get_update_ticket_price_in_order_domain = provide(UpdateTicketPriceInOrderDomain)
