import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from constants import OrderLimits
from domain.rules import EnsureUserCanCreateOrder, EnsureSessionIsOpen, EnsureSeatValidForSession
from repositories.order import OrderRepository
from repositories.seat import SeatRepository
from repositories.session import SessionRepository
from repositories.session_price import SessionPriceRepository
from repositories.ticket import TicketRepository
from repositories.unit_of_work import UnitOfWork
from schemas.booking import BookingOrderCreateReq, BookingOrderRead, BookingTicketNestedCreateReq
from schemas.order import OrderCreateDB
from services.booking import BookingDataAssembler, TicketBuilderService, OrderSchedulerService, PricingStrategy, \
    OrderTicketAdapter
from services.booking.types import SeatMap, SessionMap
from services.seat import SeatDataExistenceService
from services.session import SessionDataExistenceService
from services.session_price import SessionPriceDataExistenceService


@dataclass(frozen=True, slots=True)
class CreateBookingDataExistenceServices:
    seat: SeatDataExistenceService
    session: SessionDataExistenceService
    session_price: SessionPriceDataExistenceService


@dataclass(frozen=True, slots=True)
class CreateBookingDomain:
    user_can_create_order: EnsureUserCanCreateOrder
    session_is_open: EnsureSessionIsOpen
    seat_valid_for_session: EnsureSeatValidForSession


class CreateBookingUsage:
    def __init__(
            self,
            order_repo: OrderRepository,
            ticket_repo: TicketRepository,
            session_repo: SessionRepository,
            seat_repo: SeatRepository,
            session_price_repo: SessionPriceRepository,
            uow: UnitOfWork,

            domain: CreateBookingDomain,
            data_assembler: BookingDataAssembler,
            ticket_builder: TicketBuilderService,
            scheduler: OrderSchedulerService,
            pricing: PricingStrategy,

            data_existence: CreateBookingDataExistenceServices,
    ) -> None:
        self._order_repo = order_repo
        self._ticket_repo = ticket_repo
        self._session_repo = session_repo
        self._seat_repo = seat_repo
        self._session_price_repo = session_price_repo
        self._uow = uow

        self._domain = domain
        self._data_assembler = data_assembler
        self._pricing = pricing
        self._ticket_builder = ticket_builder
        self._scheduler = scheduler

        self._data_existence = data_existence

    async def __call__(self, data: BookingOrderCreateReq) -> BookingOrderRead:
        self._domain.user_can_create_order(
            await self._order_repo.has_active_unpaid_order(data.user_id)
        )

        session_ids = self._data_assembler.get_ids("session_id", data.tickets)
        sessions = await self._session_repo.get_many_with_movie(session_ids)
        sessions_map = self._data_assembler.build_map(sessions)
        self._data_existence.session.ensure_objs_exist(
            data.tickets,
            "session_id",
            sessions_map
        )
        self._ensure_session_is_open(sessions_map)

        seat_ids = self._data_assembler.get_ids("seat_id", data.tickets)
        seats = await self._seat_repo.get_many_with_hall(seat_ids)
        seats_map = self._data_assembler.build_map(seats)
        self._data_existence.seat.ensure_objs_exist(
            data.tickets,
            "seat_id",
            seats_map
        )

        self._ensure_seat_valid_for_session(data.tickets, sessions_map, seats_map)

        conditions = self._data_assembler.build_price_conditions(data.tickets, seats_map)
        prices = await self._session_price_repo.get_prices_by_session_and_seat_types(conditions)
        prices_map = self._data_assembler.build_prices_map(prices)
        self._data_existence.session_price.ensure_prices_exist(
            data.tickets,
            seats_map,
            prices_map
        )

        total_price = self._pricing.calculate(
            data.tickets,
            seats_map,
            prices_map,
        )

        schedule_id = str(uuid.uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=OrderLimits.EXPIRE_MINUTES
        )

        async with self._uow:
            order_create_data = OrderCreateDB(
                **data.model_dump(exclude={"tickets"}),
                expire_schedule_id=schedule_id,
                total_price=total_price,
                expires_at=expires_at
            )

            order = await self._order_repo.create(order_create_data)

            tickets = self._ticket_builder.build_many(
                order.id,
                data.tickets,
                sessions_map,
                seats_map,
                prices_map,
            )

            tickets_db = await self._ticket_repo.bulk_create(tickets)

            result = BookingOrderRead.model_validate(
                OrderTicketAdapter(order=order, tickets=tickets_db)
            )

        await self._scheduler.schedule_expiration(schedule_id, expires_at, order.id)

        return result

    def _ensure_session_is_open(self, sessions_map: SessionMap) -> None:
        for session in sessions_map.values():
            self._domain.session_is_open(
                start_time=session.start_time,
            )

    def _ensure_seat_valid_for_session(
            self,
            tickets: list[BookingTicketNestedCreateReq],
            sessions_map: SessionMap,
            seats_map: SeatMap,
    ) -> None:
        for ticket in tickets:
            session = sessions_map[ticket.session_id]
            seat = seats_map[ticket.seat_id]

            self._domain.seat_valid_for_session(
                seat_hall_id=seat.hall_id,
                session_hall_id=session.hall_id
            )
