from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, PositiveInt

from constants import SeatType, SeatLimits
from schemas.base import Id


class SeatBase(BaseModel):
    type: SeatType

    row_label: Annotated[str, Field(min_length=SeatLimits.ROW_LABEL_MIN, max_length=SeatLimits.ROW_LABEL_MAX)]
    column_label: Annotated[str, Field(min_length=SeatLimits.COLUMN_LABEL_MIN, max_length=SeatLimits.COLUMN_LABEL_MAX)]


class SeatBaseWithRelations(SeatBase):
    hall_id: PositiveInt


class SeatCreateDB(Id, SeatBaseWithRelations):
    pass


class SeatCreateReq(Id, SeatBaseWithRelations):
    pass


class SeatUpdateBase(BaseModel):
    type: SeatType | None = None

    row_label: Annotated[str | None, Field(min_length=SeatLimits.ROW_LABEL_MIN, max_length=SeatLimits.ROW_LABEL_MAX)] = None
    column_label: Annotated[str | None, Field(min_length=SeatLimits.COLUMN_LABEL_MIN, max_length=SeatLimits.COLUMN_LABEL_MAX)] = None


class SeatUpdateDB(SeatUpdateBase):
    hall_id: PositiveInt | None = None


class SeatUpdateReq(SeatUpdateBase):
    pass


class SeatRead(Id, SeatBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)
