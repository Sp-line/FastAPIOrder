from dishka.integrations.faststream import FromDishka
from pydantic import TypeAdapter

from core import (
    fs_router,
    showtimes_stream
)
from core.config import settings
from dependencies.faststream import NatsMsgIdDep
from handlers.base import base_consumer_config
from handlers.constants import SessionPriceDurables
from repositories import SessionPriceRepository
from schemas.session_price import (
    SessionPriceCreateEvent,
    SessionPriceCreateDB,
    SessionPriceUpdateEvent,
    SessionPriceUpdateDB
)
from services import InboxUnitOfWork


@fs_router.subscriber(
    "showtimes.session.prices.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SessionPriceDurables.SESSION_SVC_SESSION_PRICES_CREATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def session_prices_created_on_session_microservice_sync_db(
        payload: SessionPriceCreateEvent,
        repository: FromDishka[SessionPriceRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SessionPriceDurables.SESSION_SVC_SESSION_PRICES_CREATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.create(SessionPriceCreateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.session.prices.bulk.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SessionPriceDurables.SESSION_SVC_SESSION_PRICES_BULK_CREATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def session_prices_bulk_created_on_session_microservice_sync_db(
        payload: list[SessionPriceCreateEvent],
        repository: FromDishka[SessionPriceRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SessionPriceDurables.SESSION_SVC_SESSION_PRICES_BULK_CREATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.bulk_create(
                TypeAdapter(list[SessionPriceCreateDB]).validate_python(payload),
            )


@fs_router.subscriber(
    "showtimes.session.prices.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SessionPriceDurables.SESSION_SVC_SESSION_PRICES_UPDATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def session_prices_updated_on_session_microservice_sync_db(
        payload: SessionPriceUpdateEvent,
        repository: FromDishka[SessionPriceRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SessionPriceDurables.SESSION_SVC_SESSION_PRICES_UPDATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.update(payload.id, SessionPriceUpdateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.session.prices.bulk.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SessionPriceDurables.SESSION_SVC_SESSION_PRICES_BULK_UPDATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def session_prices_bulk_updated_on_session_microservice_sync_db(
        payload: list[SessionPriceUpdateEvent],
        repository: FromDishka[SessionPriceRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SessionPriceDurables.SESSION_SVC_SESSION_PRICES_BULK_UPDATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.bulk_update(
                {obj.id: SessionPriceUpdateDB.model_validate(obj) for obj in payload}
            )
