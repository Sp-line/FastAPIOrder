from dishka import (
    provide,
    Scope,
    Provider,
    alias
)

from services import (
    HallService,
    MovieService,
    OrderQueryService,
    OrderDataExistenceService,
    SeatService,
    SeatDataExistenceService,
    SessionService,
    SessionDataExistenceService,
    SessionPriceService,
    SessionPriceDataExistenceService,
    TicketQueryService,
    TicketDataExistenceService,
    UserService
)
from services.booking import (
    BookingDataAssembler,
    TicketBuilderService,
    DefaultPricing,
    PricingStrategy,
    OrderSchedulerService
)
from usage.booking.create_order import CreateBookingDataExistenceServices
from usage.ticket.add_ticket_to_order import AddTicketToOrderDataExistenceServices
from usage.ticket.remove_ticket_from_order import RemoveTicketFromOrderDataExistenceServices
from usage.ticket.update_ticket_status_in_order import UpdateTicketStatusInOrderDataExistenceServices


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    get_hall_service = provide(HallService)

    get_session_service = provide(SessionService)
    get_session_data_existence = provide(SessionDataExistenceService)

    get_movie_service = provide(MovieService)

    get_seat_service = provide(SeatService)
    get_seat_data_existence = provide(SeatDataExistenceService)

    get_session_price_service = provide(SessionPriceService)
    get_session_price_data_existence = provide(SessionPriceDataExistenceService)

    get_user_service = provide(UserService)

    get_order_service = provide(OrderQueryService)
    get_order_data_existence = provide(OrderDataExistenceService)

    get_ticket_query_service = provide(TicketQueryService)
    get_ticket_data_existence = provide(TicketDataExistenceService)

    get_booking_data_assembler_service = provide(BookingDataAssembler)
    get_ticket_builder_service = provide(TicketBuilderService)
    get_default_pricing = provide(DefaultPricing)
    pricing_alias = alias(source=DefaultPricing, provides=PricingStrategy)
    get_order_scheduler_service = provide(OrderSchedulerService)

    get_create_booking_data_existence_services = provide(CreateBookingDataExistenceServices)
    get_add_ticket_to_order_data_existence_services = provide(AddTicketToOrderDataExistenceServices)
    get_add_tickets_to_orders_data_existence_services = provide(AddTicketToOrderDataExistenceServices)
    get_remove_ticket_from_order_data_existence_services = provide(RemoveTicketFromOrderDataExistenceServices)
    get_update_ticket_status_in_order_data_existence_services = provide(UpdateTicketStatusInOrderDataExistenceServices)
