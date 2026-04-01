from dishka.integrations.faststream import FromDishka
from pydantic import TypeAdapter

from core import (
    fs_router,
    showtimes_stream
)
from core.config import settings
from handlers.base import base_consumer_config
from repositories import SessionPriceRepository
from repositories.unit_of_work import UnitOfWork
from schemas.session_price import (
    SessionPriceCreateEvent,
    SessionPriceCreateDB,
    SessionPriceUpdateEvent,
    SessionPriceUpdateDB
)


@fs_router.subscriber(
    "showtimes.session.prices.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_session_prices_created_sync_db",
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def session_prices_created_on_session_microservice_sync_db(
        payload: SessionPriceCreateEvent,
        repository: FromDishka[SessionPriceRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.create(SessionPriceCreateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.session.prices.bulk.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_session_prices_bulk_created_sync_db",
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def session_prices_bulk_created_on_session_microservice_sync_db(
        payload: list[SessionPriceCreateEvent],
        repository: FromDishka[SessionPriceRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.bulk_create(
            TypeAdapter(list[SessionPriceCreateDB]).validate_python(payload),
        )


@fs_router.subscriber(
    "showtimes.session.prices.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_session_prices_updated_sync_db",
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def session_prices_updated_on_session_microservice_sync_db(
        payload: SessionPriceUpdateEvent,
        repository: FromDishka[SessionPriceRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.update(payload.id, SessionPriceUpdateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.session.prices.bulk.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable="session_svc_session_prices_bulk_updated_sync_db",
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def session_prices_bulk_updated_on_session_microservice_sync_db(
        payload: list[SessionPriceUpdateEvent],
        repository: FromDishka[SessionPriceRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.bulk_update(
            {obj.id: SessionPriceUpdateDB.model_validate(obj) for obj in payload}
        )
