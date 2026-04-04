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
    UserService,
    UserDataExistenceService,
    InboxUnitOfWork
)
from services import TaskScheduler
from services.booking import (
    BookingDataAssembler,
    TicketBuilderService,
    DefaultPricing,
    PricingStrategy,
)
from usage.booking.facades import CreateBookingDataExistenceServices
from usage.order.facades import (
    BulkCreateOrderDataExistenceServices,
    CreateOrderDataExistenceServices,
    DeleteOrderDataExistenceServices,
    UpdateOrderStatusDataExistenceServices
)
from usage.ticket.facades import (
    AddTicketToOrderDataExistenceServices,
    AddTicketsToOrdersDataExistenceServices,
    RemoveTicketFromOrderDataExistenceServices,
    UpdateTicketPriceInOrderDataExistenceServices,
    UpdateTicketStatusInOrderDataExistenceServices
)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    get_inbox_unit_of_work = provide(InboxUnitOfWork)

    get_task_scheduler = provide(TaskScheduler, scope=Scope.APP)

    get_hall_service = provide(HallService)

    get_session_service = provide(SessionService)
    get_session_data_existence = provide(SessionDataExistenceService)

    get_movie_service = provide(MovieService)

    get_seat_service = provide(SeatService)
    get_seat_data_existence = provide(SeatDataExistenceService)

    get_session_price_service = provide(SessionPriceService)
    get_session_price_data_existence = provide(SessionPriceDataExistenceService)

    get_user_service = provide(UserService)
    get_user_data_existence = provide(UserDataExistenceService)

    get_order_service = provide(OrderQueryService)
    get_order_data_existence = provide(OrderDataExistenceService)

    get_ticket_query_service = provide(TicketQueryService)
    get_ticket_data_existence = provide(TicketDataExistenceService)

    get_booking_data_assembler_service = provide(BookingDataAssembler)
    get_ticket_builder_service = provide(TicketBuilderService)
    get_default_pricing = provide(DefaultPricing)
    pricing_alias = alias(source=DefaultPricing, provides=PricingStrategy)

    get_create_booking_data_existence_services = provide(CreateBookingDataExistenceServices)
    get_add_ticket_to_order_data_existence_services = provide(AddTicketToOrderDataExistenceServices)
    get_add_tickets_to_orders_data_existence_services = provide(AddTicketsToOrdersDataExistenceServices)
    get_remove_ticket_from_order_data_existence_services = provide(RemoveTicketFromOrderDataExistenceServices)
    get_update_ticket_status_in_order_data_existence_services = provide(UpdateTicketStatusInOrderDataExistenceServices)
    get_update_ticket_price_in_order_data_existence_services = provide(UpdateTicketPriceInOrderDataExistenceServices)

    get_create_order_data_existence_services = provide(CreateOrderDataExistenceServices)
    get_bulk_create_order_data_existence_services = provide(BulkCreateOrderDataExistenceServices)
    get_update_order_status_data_existence = provide(UpdateOrderStatusDataExistenceServices)
    get_delete_order_data_existence = provide(DeleteOrderDataExistenceServices)
