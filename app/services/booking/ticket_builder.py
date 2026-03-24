from __future__ import annotations

from typing import TYPE_CHECKING

from schemas.booking import BookingTicketNestedCreateReq
from schemas.ticket import (
    TicketCreateDB,
    TicketSnapshot
)

if TYPE_CHECKING:
    from core.models import Session, Seat
    from app_types import PriceMap, IntMap
    from decimal import Decimal


class TicketBuilderService:
    def build_many(
            self,
            order_id: int,
            tickets: list[BookingTicketNestedCreateReq],
            sessions_map: IntMap[Session],
            seats_map: IntMap[Seat],
            prices_map: PriceMap
    ) -> list[TicketCreateDB]:
        result: list[TicketCreateDB] = []

        for ticket in tickets:
            session = sessions_map[ticket.session_id]
            seat = seats_map[ticket.seat_id]
            price = prices_map[(ticket.session_id, seat.type)]

            result.append(
                TicketCreateDB(
                    order_id=order_id,
                    session_id=session.id,
                    seat_id=seat.id,
                    price=price.price,
                    snapshot=self._build_snapshot(session, seat),
                )
            )

        return result

    def build_one(
            self,
            order_id: int,
            session: Session,
            seat: Seat,
            price: Decimal,
    ) -> TicketCreateDB:
        return TicketCreateDB(
            order_id=order_id,
            session_id=session.id,
            seat_id=seat.id,
            price=price,
            snapshot=self._build_snapshot(session, seat),
        )

    @staticmethod
    def _build_snapshot(session: Session, seat: Seat) -> TicketSnapshot:
        return TicketSnapshot.model_validate({
            "session": session,
            "seat": seat,
            "hall": seat.hall,
            "movie": session.movie,
        })
