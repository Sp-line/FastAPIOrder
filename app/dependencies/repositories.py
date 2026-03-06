from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.hall import HallRepository
from repositories.movie import MovieRepository
from repositories.order import OrderRepository
from repositories.seat import SeatRepository
from repositories.session import SessionRepository
from repositories.session_price import SessionPriceRepository
from repositories.ticket import TicketRepository
from repositories.unit_of_work import UnitOfWork


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
    get_ticket_repo = provide(TicketRepository)
