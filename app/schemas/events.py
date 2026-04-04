from pydantic import (
    BaseModel,
    ConfigDict
)

from schemas.base import Id


class CRUDEventSchemas[
    TCreateEventSchema: BaseModel,
    TUpdateEventSchema: BaseModel,
    TDeleteEventSchema: Id,
](BaseModel):
    create: type[TCreateEventSchema]
    update: type[TUpdateEventSchema]
    delete: type[TDeleteEventSchema]

    model_config = ConfigDict(arbitrary_types_allowed=True)
