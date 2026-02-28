from datetime import datetime

from pydantic import BaseModel, PositiveInt, ConfigDict

from constants.session import DimensionFormat, ScreenTechnology
from schemas.base import Id


class SessionBase(BaseModel):
    start_time: datetime
    end_time: datetime
    dimension_format: DimensionFormat
    screen_technology: ScreenTechnology


class SessionBaseWithRelations(SessionBase):
    hall_id: PositiveInt
    movie_id: PositiveInt


class SessionCreateDB(Id, SessionBaseWithRelations):
    pass


class SessionCreateReq(Id, SessionBaseWithRelations):
    pass


class SessionUpdateBase(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    dimension_format: DimensionFormat | None = None
    screen_technology: ScreenTechnology | None = None


class SessionUpdateDB(SessionUpdateBase):
    hall_id: PositiveInt | None = None
    movie_id: PositiveInt | None = None


class SessionUpdateReq(SessionUpdateBase):
    pass


class SessionRead(Id, SessionBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)
