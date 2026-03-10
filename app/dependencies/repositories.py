from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.hall import HallRepository
from repositories.movie import MovieRepository
from repositories.order import OrderRepository
from repositories.seat import SeatRepository
from repositories.session import SessionRepository
from repositories.session_price import SessionPriceRepository
from repositories.ticket import TicketQueryRepository, TicketCommandRepository
from repositories.unit_of_work import UnitOfWork
from repositories.user import UserRepository


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_uow(self, session: AsyncSession) -> UnitOfWork:
        return UnitOfWork(session)

    get_hall_repo = provide(HallRepository)
    get_session_repo = provide(SessionRepository)
    get_movie_repo = provide(MovieRepository)
    get_seat_repo = provide(SeatRepository)
    get_session_price_repo = provide(SessionPriceRepository)
    get_order_repo = provide(OrderRepository)
    get_ticket_query_repo = provide(TicketQueryRepository)
    get_ticket_command_repo = provide(TicketCommandRepository)
    get_user_repo = provide(UserRepository)
