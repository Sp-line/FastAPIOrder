from dishka.integrations.faststream import FromDishka
from faststream import AckPolicy
from pydantic import TypeAdapter

from core import (
    fs_router,
    showtimes_stream
)
from handlers.base import base_consumer_config
from repositories import SessionRepository
from repositories.unit_of_work import UnitOfWork
from schemas.session import (
    SessionCreateEvent,
    SessionCreateDB,
    SessionUpdateEvent,
    SessionUpdateDB
)


@fs_router.subscriber(
    "showtimes.sessions.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_sessions_created_sync_db",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def sessions_created_on_session_microservice_sync_db(
        payload: SessionCreateEvent,
        repository: FromDishka[SessionRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.create(SessionCreateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.sessions.bulk.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_sessions_bulk_created_sync_db",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def sessions_bulk_created_on_session_microservice_sync_db(
        payload: list[SessionCreateEvent],
        repository: FromDishka[SessionRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.bulk_create(
            TypeAdapter(list[SessionCreateDB]).validate_python(payload),
        )


@fs_router.subscriber(
    "showtimes.sessions.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_sessions_updated_sync_db",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def sessions_updated_on_session_microservice_sync_db(
        payload: SessionUpdateEvent,
        repository: FromDishka[SessionRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.update(payload.id, SessionUpdateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.sessions.bulk.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_sessions_bulk_updated_sync_db",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def sessions_bulk_updated_on_session_microservice_sync_db(
        payload: list[SessionUpdateEvent],
        repository: FromDishka[SessionRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.bulk_update(
            {obj.id: SessionUpdateDB.model_validate(obj) for obj in payload}
        )
