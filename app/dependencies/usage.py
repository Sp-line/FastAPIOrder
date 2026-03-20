from dishka import provide, Provider, Scope

from usage.booking import GetBookingByNumberUsage, GetBookingsByUserIDUsage


class UsageProvider(Provider):
    scope = Scope.REQUEST

    get_booking_by_number_usage = provide(GetBookingByNumberUsage)
    get_bookings_by_user_id_usage = provide(GetBookingsByUserIDUsage)