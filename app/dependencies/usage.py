from dishka import provide, Provider, Scope

from usage.booking import GetBookingByNumberUsage


class UsageProvider(Provider):
    scope = Scope.REQUEST

    get_booking_by_number_usage = provide(GetBookingByNumberUsage)
