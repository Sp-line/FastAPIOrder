from dishka.integrations.faststream import FromDishka
from faststream import AckPolicy
from nats.js.api import DeliverPolicy
from pydantic import TypeAdapter

from core import (
    fs_router,
    showtimes_stream
)
from repositories import SeatRepository
from repositories.unit_of_work import UnitOfWork
from schemas.seat import (
    SeatCreateEvent,
    SeatCreateDB,
    SeatUpdateEvent,
    SeatUpdateDB
)


@fs_router.subscriber(
    "showtimes.seats.created",
    stream=showtimes_stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def seats_created_on_session_microservice_sync_db(
        payload: SeatCreateEvent,
        repository: FromDishka[SeatRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.create(SeatCreateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.seats.bulk.created",
    stream=showtimes_stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def seats_bulk_created_on_session_microservice_sync_db(
        payload: list[SeatCreateEvent],
        repository: FromDishka[SeatRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.bulk_create(
            TypeAdapter(list[SeatCreateDB]).validate_python(payload),
        )


@fs_router.subscriber(
    "showtimes.seats.updated",
    stream=showtimes_stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def seats_updated_on_session_microservice_sync_db(
        payload: SeatUpdateEvent,
        repository: FromDishka[SeatRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.update(payload.id, SeatUpdateDB(**payload.model_dump()))


@fs_router.subscriber(
    "showtimes.seats.bulk.updated",
    stream=showtimes_stream,
    deliver_policy=DeliverPolicy.NEW,
    ack_policy=AckPolicy.NACK_ON_ERROR
)
async def seats_bulk_updated_on_session_microservice_sync_db(
        payload: list[SeatUpdateEvent],
        repository: FromDishka[SeatRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.bulk_update(
            {obj.id: SeatUpdateDB.model_validate(obj) for obj in payload}
        )
