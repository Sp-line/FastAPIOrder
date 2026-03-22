from dishka import (
    provide,
    Provider,
    Scope
)

from usage.booking import GetBookingByNumberUsage, GetBookingsByUserIDUsage, CreateBookingUsage
from usage.ticket import AddTicketToOrderUsage, RemoveTicketFromOrderUsage


class UsageProvider(Provider):
    scope = Scope.REQUEST

    get_booking_create_usage = provide(CreateBookingUsage)
    get_booking_by_number_usage = provide(GetBookingByNumberUsage)
    get_bookings_by_user_id_usage = provide(GetBookingsByUserIDUsage)

    get_add_ticket_to_order_usage = provide(AddTicketToOrderUsage)
    get_remove_ticket_from_order_usage = provide(RemoveTicketFromOrderUsage)
