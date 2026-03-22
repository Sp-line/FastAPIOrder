from dataclasses import dataclass

from pydantic import TypeAdapter

from domain import (
    EnsureOrderCanBeModified,
    EnsureSessionIsOpen,
    EnsureSeatValidForSession
)
from repositories import (
    OrderRepository,
    SessionRepository,
    SeatRepository,
    SessionPriceRepository,
    TicketRepository,
    UnitOfWork
)
from schemas.order import OrderUpdateDB
from schemas.ticket import (
    TicketCreateReq,
    TicketRead, TicketCreateDB
)
from services import (
    OrderDataExistenceService,
    SeatDataExistenceService,
    SessionDataExistenceService,
    SessionPriceDataExistenceService
)
from services.booking import (
    BookingDataAssembler,
    TicketBuilderService,
    PricingStrategy
)
from services.booking.types import (
    SessionMap,
    OrderMap,
    SeatMap
)


@dataclass(frozen=True, slots=True)
class AddTicketsToOrdersDataExistenceServices:
    order: OrderDataExistenceService
    seat: SeatDataExistenceService
    session: SessionDataExistenceService
    session_price: SessionPriceDataExistenceService


@dataclass(frozen=True, slots=True)
class AddTicketsToOrdersDomain:
    order_can_be_modified: EnsureOrderCanBeModified
    session_is_open: EnsureSessionIsOpen
    seat_valid_for_session: EnsureSeatValidForSession


class AddTicketsToOrdersUsage:
    def __init__(
            self,
            order_repo: OrderRepository,
            session_repo: SessionRepository,
            seat_repo: SeatRepository,
            session_price_repo: SessionPriceRepository,
            ticket_repo: TicketRepository,
            unit_of_work: UnitOfWork,

            domain: AddTicketsToOrdersDomain,
            data_assembler: BookingDataAssembler,
            ticket_builder: TicketBuilderService,
            pricing: PricingStrategy,

            data_existence: AddTicketsToOrdersDataExistenceServices,
    ) -> None:
        self._order_repo = order_repo
        self._session_repo = session_repo
        self._seat_repo = seat_repo
        self._session_price_repo = session_price_repo
        self._ticket_repo = ticket_repo
        self._uow = unit_of_work

        self._domain = domain
        self._data_assembler = data_assembler
        self._ticket_builder = ticket_builder
        self._pricing = pricing

        self._data_existence = data_existence

    async def __call__(self, data: list[TicketCreateReq]) -> list[TicketRead]:
        if not data:
            return []

        order_ids = self._data_assembler.get_ids(data, "order_id")
        orders = await self._order_repo.get_by_ids(order_ids)
        orders_map = self._data_assembler.build_map(orders)
        self._data_existence.order.ensure_objs_exist(data, "order_id", orders_map)
        self._ensure_orders_can_be_modified(orders_map)

        session_ids = self._data_assembler.get_ids(data, "session_id")
        sessions = await self._session_repo.get_many_with_movie(session_ids)
        sessions_map = self._data_assembler.build_map(sessions)
        self._data_existence.session.ensure_objs_exist(data, "session_id", sessions_map)
        self._ensure_sessions_are_open(sessions_map)

        seat_ids = self._data_assembler.get_ids(data, "seat_id")
        seats = await self._seat_repo.get_many_with_hall(seat_ids)
        seats_map = self._data_assembler.build_map(seats)
        self._data_existence.seat.ensure_objs_exist(data, "seat_id", seats_map)

        self._ensure_seats_valid_for_sessions(data, sessions_map, seats_map)

        conditions = self._data_assembler.build_price_conditions(data, seats_map)
        prices = await self._session_price_repo.get_prices_by_session_and_seat_types(conditions)
        prices_map = self._data_assembler.build_prices_map(prices)
        self._data_existence.session_price.ensure_prices_exist(data, seats_map, prices_map)

        tickets_create: list[TicketCreateDB] = []
        updated_order_prices = {order_id: order.total_price for order_id, order in orders_map.items()}

        for ticket in data:
            session = sessions_map[ticket.session_id]
            seat = seats_map[ticket.seat_id]
            price_key = (ticket.session_id, seat.type)
            price = prices_map[price_key]

            ticket_create = self._ticket_builder.build_one(
                    order_id=ticket.order_id,
                    session=session,
                    seat=seat,
                    price=price.price
                )
            tickets_create.append(ticket_create)

            updated_order_prices[ticket.order_id] = self._pricing.increment_by_one(
                order_total_price=updated_order_prices[ticket.order_id],
                new_ticket_price=price.price
            )

        adapter = TypeAdapter(list[TicketRead])

        async with self._uow:
            tickets = await self._ticket_repo.bulk_create(tickets_create)

            orders_update: dict[int, OrderUpdateDB] = {}
            for order_id, new_total_price in updated_order_prices.items():
                if new_total_price != orders_map[order_id].total_price:
                    orders_update[order_id] = OrderUpdateDB(total_price=new_total_price)

            if orders_update:
                await self._order_repo.bulk_update(orders_update)

            return adapter.validate_python(tickets)


    def _ensure_orders_can_be_modified(self, orders_map: OrderMap) -> None:
        for order in orders_map.values():
            self._domain.order_can_be_modified(order.status)


    def _ensure_sessions_are_open(self, sessions_map: SessionMap) -> None:
        for session in sessions_map.values():
            self._domain.session_is_open(start_time=session.start_time)

    def _ensure_seats_valid_for_sessions(
            self,
            tickets: list[TicketCreateReq],
            sessions_map: SessionMap,
            seats_map: SeatMap,
    ) -> None:
        for t in tickets:
            session = sessions_map[t.session_id]
            seat = seats_map[t.seat_id]

            self._domain.seat_valid_for_session(
                seat_hall_id=seat.hall_id,
                session_hall_id=session.hall_id
            )
