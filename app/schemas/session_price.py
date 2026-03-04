from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt, ConfigDict

from constants import SeatType, SessionPriceLimits
from schemas.base import Id


class SessionPriceBase(BaseModel):
    seat_type: SeatType
    price: Annotated[Decimal, Field(ge=SessionPriceLimits.PRICE_MIN)]


class SessionPriceBaseWithRelations(SessionPriceBase):
    session_id: PositiveInt


class SessionPriceCreateReq(Id, SessionPriceBaseWithRelations):
    pass


class SessionPriceCreateDB(SessionPriceCreateReq):
    pass


class SessionPriceUpdateBase(BaseModel):
    seat_type: SeatType | None = None
    price: Annotated[Decimal | None, Field(ge=SessionPriceLimits.PRICE_MIN)] = None


class SessionPriceUpdateReq(SessionPriceUpdateBase):
    pass


class SessionPriceUpdateDB(SessionPriceUpdateReq):
    session_id: PositiveInt | None = None


class SessionPriceRead(Id, SessionPriceBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)


class SessionPriceCombination(BaseModel):
    session_id: PositiveInt
    seat_type: SeatType

    model_config = ConfigDict(frozen=True)
