from dishka import provide, Scope, Provider

from service.hall import HallService
from service.movie import MovieService
from service.seat import SeatService
from service.session import SessionService
from service.session_price import SessionPriceService
from service.ticket import TicketQueryService
from service.user import UserService
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
