from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from constants import InboxEventLimits
from schemas.base import Id


class InboxEventBase(BaseModel):
    code: UUID
    handler: Annotated[str, Field(min_length=InboxEventLimits.HANDLER_MIN, max_length=InboxEventLimits.HANDLER_MAX)]


class InboxEventCreateReq(InboxEventBase):
    pass


class InboxEventCreateDB(InboxEventBase):
    pass


class InboxEventUpdateBase(BaseModel):
    code: UUID | None = None
    handler: Annotated[str | None, Field(min_length=InboxEventLimits.HANDLER_MIN, max_length=InboxEventLimits.HANDLER_MAX)] = None


class InboxEventUpdateReq(InboxEventUpdateBase):
    pass


class InboxEventUpdateDB(InboxEventUpdateReq):
    pass


class InboxEventRead(Id, InboxEventBase):
    model_config = ConfigDict(from_attributes=True)
