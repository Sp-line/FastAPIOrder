from dishka.integrations.faststream import FromDishka
from pydantic import TypeAdapter

from core import (
    fs_router,
    showtimes_stream
)
from core.config import settings
from handlers.base import base_consumer_config
from repositories import HallRepository
from repositories.unit_of_work import UnitOfWork
from schemas.hall import (
    HallCreateEvent,
    HallCreateDB,
    HallUpdateEvent,
    HallUpdateDB
)


@fs_router.subscriber(
    "showtimes.halls.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_halls_created_sync_db",
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def halls_created_on_session_microservice_sync_db(
        payload: HallCreateEvent,
        repository: FromDishka[HallRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.create(HallCreateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.halls.bulk.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_halls_bulk_created_sync_db",
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def halls_bulk_created_on_session_microservice_sync_db(
        payload: list[HallCreateEvent],
        repository: FromDishka[HallRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.bulk_create(
            TypeAdapter(list[HallCreateDB]).validate_python(payload),
        )


@fs_router.subscriber(
    "showtimes.halls.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_halls_updated_sync_db",
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def halls_updated_on_session_microservice_sync_db(
        payload: HallUpdateEvent,
        repository: FromDishka[HallRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.update(payload.id, HallUpdateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.halls.bulk.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_halls_bulk_updated_sync_db",
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def halls_bulk_updated_on_session_microservice_sync_db(
        payload: list[HallUpdateEvent],
        repository: FromDishka[HallRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.bulk_update(
            {obj.id: HallUpdateDB.model_validate(obj) for obj in payload}
        )
