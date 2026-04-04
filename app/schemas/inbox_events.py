from uuid import UUID

from pydantic import BaseModel, ConfigDict

from schemas.base import Id


class InboxEventBase(BaseModel):
    code: UUID


class InboxEventCreateReq(Id, InboxEventBase):
    pass


class InboxEventCreateDB(InboxEventBase):
    pass


class InboxEventUpdateBase(BaseModel):
    code: UUID | None = None


class InboxEventUpdateReq(InboxEventUpdateBase):
    pass


class InboxEventUpdateDB(InboxEventUpdateReq):
    pass


class InboxEventRead(Id, InboxEventUpdateBase):
    model_config = ConfigDict(from_attributes=True)
