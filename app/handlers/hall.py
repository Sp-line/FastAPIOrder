from dishka.integrations.faststream import FromDishka
from pydantic import TypeAdapter

from core import (
    fs_router,
    showtimes_stream
)
from core.config import settings
from dependencies.faststream import NatsMsgIdDep
from handlers.base import base_consumer_config
from handlers.constants import HallDurables
from repositories import HallRepository
from schemas.hall import (
    HallCreateEvent,
    HallCreateDB,
    HallUpdateEvent,
    HallUpdateDB
)
from services import InboxUnitOfWork


@fs_router.subscriber(
    "showtimes.halls.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable=HallDurables.ORDER_SVC_HALLS_CREATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def halls_created_on_session_microservice_sync_db(
        payload: HallCreateEvent,
        repository: FromDishka[HallRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=HallDurables.ORDER_SVC_HALLS_CREATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.create(HallCreateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.halls.bulk.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable=HallDurables.ORDER_SVC_HALLS_BULK_CREATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def halls_bulk_created_on_session_microservice_sync_db(
        payload: list[HallCreateEvent],
        repository: FromDishka[HallRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=HallDurables.ORDER_SVC_HALLS_BULK_CREATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.bulk_create(
                TypeAdapter(list[HallCreateDB]).validate_python(payload),
            )


@fs_router.subscriber(
    "showtimes.halls.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable=HallDurables.ORDER_SVC_HALLS_UPDATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def halls_updated_on_session_microservice_sync_db(
        payload: HallUpdateEvent,
        repository: FromDishka[HallRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=HallDurables.ORDER_SVC_HALLS_UPDATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.update(payload.id, HallUpdateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.halls.bulk.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable=HallDurables.ORDER_SVC_HALLS_BULK_UPDATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def halls_bulk_updated_on_session_microservice_sync_db(
        payload: list[HallUpdateEvent],
        repository: FromDishka[HallRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=HallDurables.ORDER_SVC_HALLS_BULK_UPDATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.bulk_update(
                {obj.id: HallUpdateDB.model_validate(obj) for obj in payload}
            )
