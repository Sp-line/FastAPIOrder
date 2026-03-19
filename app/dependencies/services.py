from dishka import provide, Scope, Provider, alias

from domain.booking import BookingDomain
from services.booking import BookingDataAssembler, TicketBuilderService, DefaultPricing, PricingStrategy, \
    OrderSchedulerService
from services.hall import HallService
from services.movie import MovieService
from services.seat import SeatService
from services.session import SessionService
from services.session_price import SessionPriceService
from services.ticket import TicketQueryService
from services.user import UserService


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    get_hall_service = provide(HallService)

    get_session_service = provide(SessionService)

    get_movie_service = provide(MovieService)

    get_seat_service = provide(SeatService)

    get_session_price_service = provide(SessionPriceService)

    get_user_service = provide(UserService)
    get_ticket_query_service = provide(TicketQueryService)

    get_booking_domain_service = provide(BookingDomain)
    get_booking_data_assembler_service = provide(BookingDataAssembler)
    get_ticket_builder_service = provide(TicketBuilderService)
    get_default_pricing = provide(DefaultPricing)
    pricing_alias = alias(source=DefaultPricing, provides=PricingStrategy)
    get_order_scheduler_service = provide(OrderSchedulerService)
