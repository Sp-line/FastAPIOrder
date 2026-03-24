from dishka import (
    provide,
    Provider,
    Scope
)

from usage.booking import (
    GetBookingByNumberUsage,
    GetBookingsByUserIDUsage,
    CreateBookingUsage,
    GetTicketByPublicCodeUsage,
    GetTicketsByUserIdUsage
)
from usage.order import (
    OrderCreateUsage,
    BulkCreateOrderUsage,
    UpdateOrderStatusUsage
)
from usage.ticket import (
    AddTicketToOrderUsage,
    RemoveTicketFromOrderUsage,
    UpdateTicketStatusInOrderUsage,
    UpdateTicketPriceInOrderUsage
)


class UsageProvider(Provider):
    scope = Scope.REQUEST

    get_booking_create_usage = provide(CreateBookingUsage)
    get_booking_by_number_usage = provide(GetBookingByNumberUsage)
    get_bookings_by_user_id_usage = provide(GetBookingsByUserIDUsage)
    get_ticket_by_public_code_usage = provide(GetTicketByPublicCodeUsage)
    get_tickets_by_user_id_usage = provide(GetTicketsByUserIdUsage)

    get_add_ticket_to_order_usage = provide(AddTicketToOrderUsage)
    get_remove_ticket_from_order_usage = provide(RemoveTicketFromOrderUsage)
    get_update_ticket_status_in_order_usage = provide(UpdateTicketStatusInOrderUsage)
    get_update_ticket_price_in_order_usage = provide(UpdateTicketPriceInOrderUsage)

    get_create_order_usage = provide(OrderCreateUsage)
    get_bulk_create_order_usage = provide(BulkCreateOrderUsage)
    get_update_order_status_usage = provide(UpdateOrderStatusUsage)
