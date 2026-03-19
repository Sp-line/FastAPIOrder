from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, PositiveInt, Field, field_validator, ConfigDict

from constants import TicketStatus, TicketLimits, BookingLimits
from schemas.order import OrderRead
from schemas.ticket import TicketSnapshot


class BookingTicketNestedCreateReq(BaseModel):
    session_id: PositiveInt
    seat_id: PositiveInt


class BookingOrderCreateReq(BaseModel):
    user_id: PositiveInt
    tickets: Annotated[list[BookingTicketNestedCreateReq], Field(min_length=BookingLimits.TICKETS_PER_ORDER_MIN, max_length=BookingLimits.TICKETS_PER_ORDER_MAX)]

    @field_validator("tickets")
    @classmethod
    def check_no_duplicates(cls, tickets: list[BookingTicketNestedCreateReq]) -> list[BookingTicketNestedCreateReq]:
        unique_tickets = {(t.session_id, t.seat_id) for t in tickets}
        if len(unique_tickets) != len(tickets):
            raise ValueError("The cart contains duplicate tickets for the same seat.")
        return tickets


class BookingTicketNestedRead(BaseModel):
    session_id: PositiveInt
    seat_id: PositiveInt

    public_code: UUID

    status: TicketStatus
    price: Annotated[Decimal, Field(ge=TicketLimits.PRICE_MIN)]
    snapshot: TicketSnapshot

    model_config = ConfigDict(from_attributes=True)


class BookingOrderRead(OrderRead):
    tickets: Annotated[list[BookingTicketNestedRead], Field(min_length=BookingLimits.TICKETS_PER_ORDER_MIN, max_length=BookingLimits.TICKETS_PER_ORDER_MAX)]

    model_config = ConfigDict(from_attributes=True)
