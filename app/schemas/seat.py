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


class SeatCreateReq(Id, SeatBaseWithRelations):
    pass


class SeatCreateDB(SeatCreateReq):
    pass


class SeatUpdateBase(BaseModel):
    type: SeatType | None = None

    row_label: Annotated[str | None, Field(min_length=SeatLimits.ROW_LABEL_MIN, max_length=SeatLimits.ROW_LABEL_MAX)] = None
    column_label: Annotated[str | None, Field(min_length=SeatLimits.COLUMN_LABEL_MIN, max_length=SeatLimits.COLUMN_LABEL_MAX)] = None


class SeatUpdateReq(SeatUpdateBase):
    pass


class SeatUpdateDB(SeatUpdateReq):
    hall_id: PositiveInt | None = None


class SeatRead(Id, SeatBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)


class SeatSnapshot(Id, SeatBase):
    model_config = ConfigDict(from_attributes=True)
