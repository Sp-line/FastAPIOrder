from typing import Annotated, TypeAlias
from uuid import UUID

from fastapi import Depends
from faststream.nats.fastapi import Context

# noinspection PyUnresolvedReferences
NatsMsgIdStrDep: TypeAlias = Annotated[
    str | None,
    Context("message.headers.Nats-Msg-Id", default=None),
]


async def get_nats_msg_id_uuid(msg_id: NatsMsgIdStrDep) -> UUID | None:
    if msg_id is not None:
        return UUID(msg_id.strip('"'))
    return None


NatsMsgIdDep: TypeAlias = Annotated[UUID | None, Depends(get_nats_msg_id_uuid)]
