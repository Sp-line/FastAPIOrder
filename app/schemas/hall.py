from typing import Annotated

from pydantic import ConfigDict, BaseModel, Field

from constants import HallLimits
from schemas.base import Id


class HallBase(BaseModel):
    name: Annotated[str, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)]
    slug: Annotated[str, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)]


class HallCreateReq(Id, HallBase):
    pass


class HallCreateDB(HallCreateReq):
    pass


class HallUpdateBase(BaseModel):
    name: Annotated[str | None, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)] = None
    slug: Annotated[str | None, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)] = None


class HallUpdateReq(HallUpdateBase):
    pass


class HallUpdateDB(HallUpdateReq):
    pass


class HallRead(Id, HallBase):
    model_config = ConfigDict(from_attributes=True)


class HallSnapshot(HallRead):
    model_config = ConfigDict(from_attributes=True)


class HallCreateEvent(HallCreateDB):
    model_config = ConfigDict(extra='ignore')


class HallUpdateEvent(Id, HallUpdateDB):
    model_config = ConfigDict(extra='ignore')
