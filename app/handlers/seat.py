from dishka.integrations.faststream import FromDishka
from pydantic import TypeAdapter

from core import (
    fs_router,
    showtimes_stream
)
from core.config import settings
from dependencies.faststream import NatsMsgIdDep
from handlers.base import base_consumer_config
from handlers.constants import SeatDurables
from repositories import SeatRepository
from schemas.seat import (
    SeatCreateEvent,
    SeatCreateDB,
    SeatUpdateEvent,
    SeatUpdateDB
)
from services import InboxUnitOfWork


@fs_router.subscriber(
    "showtimes.seats.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SeatDurables.SESSION_SVC_SEATS_CREATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def seats_created_on_session_microservice_sync_db(
        payload: SeatCreateEvent,
        repository: FromDishka[SeatRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SeatDurables.SESSION_SVC_SEATS_CREATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.create(SeatCreateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.seats.bulk.created",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SeatDurables.SESSION_SVC_SEATS_BULK_CREATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def seats_bulk_created_on_session_microservice_sync_db(
        payload: list[SeatCreateEvent],
        repository: FromDishka[SeatRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SeatDurables.SESSION_SVC_SEATS_BULK_CREATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.bulk_create(
                TypeAdapter(list[SeatCreateDB]).validate_python(payload),
            )


@fs_router.subscriber(
    "showtimes.seats.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SeatDurables.SESSION_SVC_SEATS_UPDATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def seats_updated_on_session_microservice_sync_db(
        payload: SeatUpdateEvent,
        repository: FromDishka[SeatRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SeatDurables.SESSION_SVC_SEATS_UPDATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.update(payload.id, SeatUpdateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.seats.bulk.updated",
    stream=showtimes_stream,
    pull_sub=True,
    durable=SeatDurables.SESSION_SVC_SEATS_BULK_UPDATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def seats_bulk_updated_on_session_microservice_sync_db(
        payload: list[SeatUpdateEvent],
        repository: FromDishka[SeatRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=SeatDurables.SESSION_SVC_SEATS_BULK_UPDATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.bulk_update(
                {obj.id: SeatUpdateDB.model_validate(obj) for obj in payload}
            )
