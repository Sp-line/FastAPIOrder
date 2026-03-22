from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from domain.rules import (
    EnsureSessionIsOpen,
    EnsureOrderCanBeModified,
    EnsureSeatValidForSession,
)
from repositories.order import OrderRepository
from repositories.seat import SeatRepository
from repositories.session import SessionRepository
from repositories.session_price import SessionPriceRepository
from repositories.ticket import TicketRepository
from repositories.unit_of_work import UnitOfWork
from schemas.order import OrderUpdateDB
from schemas.ticket import TicketCreateReq, TicketRead
from services.booking import TicketBuilderService, PricingStrategy
from services.order import OrderDataExistenceService
from services.seat import SeatDataExistenceService
from services.session import SessionDataExistenceService
from services.session_price import SessionPriceDataExistenceService

if TYPE_CHECKING:
    from core.models import Order, Seat, Session


@dataclass(frozen=True, slots=True)
class AddTicketToOrderDataExistenceServices:
    seat: SeatDataExistenceService
    session: SessionDataExistenceService
    order: OrderDataExistenceService
    session_price: SessionPriceDataExistenceService


@dataclass(frozen=True, slots=True)
class AddTicketToOrderDomain:
    order_can_be_modified: EnsureOrderCanBeModified
    session_is_open: EnsureSessionIsOpen
    seat_valid_for_session: EnsureSeatValidForSession


class AddTicketToOrderUsage:
    def __init__(
            self,
            order_repo: OrderRepository,
            session_repo: SessionRepository,
            seat_repo: SeatRepository,
            session_price_repo: SessionPriceRepository,
            ticket_repo: TicketRepository,
            unit_of_work: UnitOfWork,

            domain: AddTicketToOrderDomain,
            ticket_builder: TicketBuilderService,
            pricing: PricingStrategy,

            data_existence_services: AddTicketToOrderDataExistenceServices,
    ) -> None:
        self._order_repo = order_repo
        self._session_repo = session_repo
        self._seat_repo = seat_repo
        self._session_price_repo = session_price_repo
        self._ticket_repo = ticket_repo
        self._uow = unit_of_work

        self._domain = domain
        self._ticket_builder = ticket_builder
        self._pricing = pricing

        self._data_existence_services = data_existence_services

    async def __call__(self, data: TicketCreateReq) -> TicketRead:
        order = self._data_existence_services.order.ensure_obj_exist(
            data.order_id,
            await self._order_repo.get_by_id(data.order_id)
        )
        self._ensure_order_can_be_modified(order)

        session = self._data_existence_services.session.ensure_obj_exist(
            data.session_id,
            await self._session_repo.get_with_movie(data.session_id)
        )
        self._ensure_session_is_open(session)

        seat = self._data_existence_services.seat.ensure_obj_exist(
            data.seat_id,
            await self._seat_repo.get_with_hall(data.seat_id),
        )

        self._ensure_seat_valid_for_session(seat, session)

        price = self._data_existence_services.session_price.ensure_price_exist(
            session.id,
            seat.type,
            await self._session_price_repo.get_price_for_seat_type(
                session_id=session.id,
                seat_type=seat.type
            )
        )

        async with self._uow:
            ticket_create_data = self._ticket_builder.build_one(
                order_id=order.id,
                session=session,
                seat=seat,
                price=price,
            )

            ticket = await self._ticket_repo.create(ticket_create_data)

            await self._order_repo.update(
                obj_id=order.id,
                data=OrderUpdateDB(
                    total_price=self._pricing.increment_by_one(
                        order_total_price=order.total_price,
                        new_ticket_price=ticket.price
                    )
                )
            )

            return TicketRead.model_validate(ticket)

    def _ensure_order_can_be_modified(self, order: Order) -> None:
        self._domain.order_can_be_modified(
            order_status=order.status,
        )

    def _ensure_session_is_open(self, session: Session) -> None:
        self._domain.session_is_open(
            start_time=session.start_time,
        )

    def _ensure_seat_valid_for_session(self, seat: Seat, session: Session) -> None:
        self._domain.seat_valid_for_session(
            seat_hall_id=seat.hall_id,
            session_hall_id=session.hall_id
        )
