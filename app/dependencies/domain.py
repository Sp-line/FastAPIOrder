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
)
from usage.booking.create_order import CreateBookingDomain
from usage.ticket.add_ticket_to_order import AddTicketToOrderDomain
from usage.ticket.add_tickets_to_orders import AddTicketsToOrdersDomain
from usage.ticket.remove_ticket_from_order import RemoveTicketFromOrderDomain


class DomainProvider(Provider):
    scope = Scope.APP

    get_ensure_order_can_be_modified = provide(EnsureOrderCanBeModified)
    get_ensure_seat_valid_for_session = provide(EnsureSeatValidForSession)
    get_ensure_user_can_create_order = provide(EnsureUserCanCreateOrder)

    @provide
    def get_ensure_session_is_open(self) -> EnsureSessionIsOpen:
        return EnsureSessionIsOpen()

    get_create_booking_domain = provide(CreateBookingDomain)

    get_add_ticket_to_order_domain = provide(AddTicketToOrderDomain)
    get_add_tickets_to_orders_domain = provide(AddTicketsToOrdersDomain)
    get_remove_ticket_from_order_domain = provide(RemoveTicketFromOrderDomain)
