from dishka import (
    Provider,
    Scope,
    provide
)

from repositories import (
    UnitOfWork,
    HallRepository,
    SessionRepository,
    MovieRepository,
    SeatRepository,
    SessionPriceRepository,
    OrderQueryRepository,
    OrderCommandRepository,
    OrderRepository,
    UserRepository,
    TicketQueryRepository,
    TicketCommandRepository,
    TicketRepository,
)


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    get_uow = provide(UnitOfWork)

    get_hall_repo = provide(HallRepository)

    get_session_repo = provide(SessionRepository)

    get_movie_repo = provide(MovieRepository)

    get_seat_repo = provide(SeatRepository)

    get_session_price_repo = provide(SessionPriceRepository)

    get_order_query_repo = provide(OrderQueryRepository)
    get_order_command_repo = provide(OrderCommandRepository)
    get_order_repo = provide(OrderRepository)

    get_user_repo = provide(UserRepository)

    get_ticket_query_repo = provide(TicketQueryRepository)
    get_ticket_command_repo = provide(TicketCommandRepository)
    get_ticket_repository = provide(TicketRepository)
