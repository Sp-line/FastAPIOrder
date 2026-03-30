from decimal import Decimal
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, PositiveInt, Field, ConfigDict

from constants import TicketStatus, TicketLimits
from schemas.base import Id
from schemas.events import CRUDEventSchemas
from schemas.hall import HallSnapshot
from schemas.movie import MovieSnapshot
from schemas.seat import SeatSnapshot
from schemas.session import SessionSnapshot


class TicketSnapshot(BaseModel):
    seat: SeatSnapshot
    hall: HallSnapshot
    session: SessionSnapshot
    movie: MovieSnapshot

    model_config = ConfigDict(from_attributes=True)


class TicketBase(BaseModel):
    pass


class TicketBaseWithRelations(TicketBase):
    order_id: PositiveInt
    session_id: PositiveInt
    seat_id: PositiveInt


class TicketCreateReq(TicketBaseWithRelations):
    pass


class TicketCreateDB(TicketCreateReq):
    public_code: UUID = Field(default_factory=uuid4)

    status: TicketStatus = TicketStatus.RESERVED
    price: Annotated[Decimal, Field(ge=TicketLimits.PRICE_MIN)]
    snapshot: TicketSnapshot


class TicketUpdateBase(BaseModel):
    pass


class TicketUpdateReq(TicketUpdateBase):
    pass


class TicketUpdateDB(TicketUpdateReq):
    public_code: UUID | None = None

    status: TicketStatus | None = None
    price: Annotated[Decimal | None, Field(ge=TicketLimits.PRICE_MIN)] = None
    snapshot: TicketSnapshot | None = None

    order_id: PositiveInt | None = None
    session_id: PositiveInt | None = None
    seat_id: PositiveInt | None = None


class TicketRead(TicketBaseWithRelations):
    public_code: UUID

    status: TicketStatus
    price: Annotated[Decimal, Field(ge=TicketLimits.PRICE_MIN)]
    snapshot: TicketSnapshot

    model_config = ConfigDict(from_attributes=True)


class TicketAdminRead(Id, TicketRead):
    model_config = ConfigDict(from_attributes=True)


class TicketStatusUpdateReq(BaseModel):
    status: TicketStatus


class TicketPriceUpdateReq(BaseModel):
    price: Annotated[Decimal, Field(ge=TicketLimits.PRICE_MIN)]


class TicketCreateEvent(TicketAdminRead):
    model_config = ConfigDict(extra='ignore')


class TicketUpdateEvent(TicketAdminRead):
    model_config = ConfigDict(extra='ignore')


class TicketDeleteEvent(Id, TicketBaseWithRelations):
    model_config = ConfigDict(extra='ignore')


ticket_event_schemas = CRUDEventSchemas[
    TicketCreateEvent,
    TicketUpdateEvent,
    TicketDeleteEvent
](
    create=TicketCreateEvent,
    update=TicketUpdateEvent,
    delete=TicketDeleteEvent
)
