from typing import TypeAlias, Annotated
from uuid import UUID

from faststream.nats.fastapi import Context

# noinspection PyUnresolvedReferences
NatsMsgIdDep: TypeAlias = Annotated[UUID | None, Context("message.headers.Nats-Msg-Id", default=None)]
