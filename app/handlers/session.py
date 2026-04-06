from dishka.integrations.faststream import FromDishka
from pydantic import TypeAdapter

from core import (
    fs_router,
    showtimes_stream
)
from core.config import settings
from dependencies.faststream import NatsMsgIdDep
from handlers.base import base_consumer_config
from handlers.constants import SessionDurables
from repositories import SessionRepository
from schemas.session import (
    SessionCreateEvent,
    SessionCreateDB,
    SessionUpdateEvent,
    SessionUpdateDB
)
from services import InboxUnitOfWork


@fs_router.subscriber(
    "showtimes.sessions.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SessionDurables.SESSION_SVC_SESSIONS_CREATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def sessions_created_on_session_microservice_sync_db(
        payload: SessionCreateEvent,
        repository: FromDishka[SessionRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SessionDurables.SESSION_SVC_SESSIONS_CREATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.create(SessionCreateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.sessions.bulk.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SessionDurables.SESSION_SVC_SESSIONS_BULK_CREATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def sessions_bulk_created_on_session_microservice_sync_db(
        payload: list[SessionCreateEvent],
        repository: FromDishka[SessionRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SessionDurables.SESSION_SVC_SESSIONS_BULK_CREATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.bulk_create(
                TypeAdapter(list[SessionCreateDB]).validate_python(payload),
            )


@fs_router.subscriber(
    "showtimes.sessions.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SessionDurables.SESSION_SVC_SESSIONS_UPDATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def sessions_updated_on_session_microservice_sync_db(
        payload: SessionUpdateEvent,
        repository: FromDishka[SessionRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SessionDurables.SESSION_SVC_SESSIONS_UPDATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.update(payload.id, SessionUpdateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.sessions.bulk.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SessionDurables.SESSION_SVC_SESSIONS_BULK_UPDATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def sessions_bulk_updated_on_session_microservice_sync_db(
        payload: list[SessionUpdateEvent],
        repository: FromDishka[SessionRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SessionDurables.SESSION_SVC_SESSIONS_BULK_UPDATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.bulk_update(
                {obj.id: SessionUpdateDB.model_validate(obj) for obj in payload}
            )
