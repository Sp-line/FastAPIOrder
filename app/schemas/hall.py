from typing import Annotated

from pydantic import ConfigDict, BaseModel, Field

from constants import HallLimits
from schemas.base import Id


class HallBase(BaseModel):
    name: Annotated[str, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)]
    slug: Annotated[str, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)]


class HallCreateDB(Id, HallBase):
    pass


class HallCreateReq(Id, HallBase):
    pass


class HallUpdateBase(BaseModel):
    name: Annotated[str | None, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)] = None
    slug: Annotated[str | None, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)] = None


class HallUpdateDB(HallUpdateBase):
    pass


class HallUpdateReq(HallUpdateBase):
    pass


class HallRead(Id, HallBase):
    model_config = ConfigDict(from_attributes=True)