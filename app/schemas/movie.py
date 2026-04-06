from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import MovieLimits
from schemas.base import Id


class MovieBase(BaseModel):
    title: Annotated[str, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)]
    slug: Annotated[str, Field(min_length=MovieLimits.SLUG_MIN, max_length=MovieLimits.SLUG_MAX)]


class MovieCreateReq(Id, MovieBase):
    pass


class MovieCreateDB(MovieCreateReq):
    pass


class MovieUpdateBase(BaseModel):
    title: Annotated[str | None, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)] = None
    slug: Annotated[str | None, Field(min_length=MovieLimits.SLUG_MIN, max_length=MovieLimits.SLUG_MAX)] = None


class MovieUpdateReq(MovieUpdateBase):
    pass


class MovieUpdateDB(MovieUpdateReq):
    pass


class MovieRead(Id, MovieBase):
    model_config = ConfigDict(from_attributes=True)


class MovieSnapshot(MovieRead):
    model_config = ConfigDict(from_attributes=True)


class MovieCreateEvent(MovieRead):
    model_config = ConfigDict(extra='ignore')


class MovieUpdateEvent(MovieRead):
    model_config = ConfigDict(extra='ignore')
