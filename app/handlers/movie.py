from dishka.integrations.faststream import FromDishka
from pydantic import TypeAdapter

from core import (
    fs_router,
    catalog_stream
)
from core.config import settings
from dependencies.faststream import NatsMsgIdDep
from handlers.base import base_consumer_config
from handlers.constants import MovieDurables
from repositories.movie import MovieRepository
from schemas.movie import (
    MovieCreateEvent,
    MovieCreateDB,
    MovieUpdateEvent,
    MovieUpdateDB
)
from services import InboxUnitOfWork


@fs_router.subscriber(
    "catalog.movies.created",
    stream=catalog_stream,
    pull_sub=True,
    durable=MovieDurables.MOVIE_SVC_MOVIES_CREATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def movies_created_on_movie_microservice_sync_db(
        payload: MovieCreateEvent,
        repository: FromDishka[MovieRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=MovieDurables.MOVIE_SVC_MOVIES_CREATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.create(MovieCreateDB(**payload.model_dump()))


@fs_router.subscriber(
    "catalog.movies.bulk.created",
    stream=catalog_stream,
    pull_sub=True,
    durable=MovieDurables.MOVIE_SVC_MOVIES_BULK_CREATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def movies_bulk_created_on_movie_microservice_sync_db(
        payload: list[MovieCreateEvent],
        repository: FromDishka[MovieRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=MovieDurables.MOVIE_SVC_MOVIES_BULK_CREATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.bulk_create(
                TypeAdapter(list[MovieCreateDB]).validate_python(payload),
            )


@fs_router.subscriber(
    "catalog.movies.updated",
    stream=catalog_stream,
    pull_sub=True,
    durable=MovieDurables.MOVIE_SVC_MOVIES_UPDATED_SYNC_DB,
    ack_policy=settings.faststream.consumer.faststream_ack_policy,
    config=base_consumer_config
)
async def movies_updated_on_movie_microservice_sync_db(
        payload: MovieUpdateEvent,
        repository: FromDishka[MovieRepository],
        inbox_unit_of_work: FromDishka[InboxUnitOfWork],
        msg_id: NatsMsgIdDep
) -> None:
    async with inbox_unit_of_work.transactional(
            msg_id=msg_id,
            handler=MovieDurables.MOVIE_SVC_MOVIES_UPDATED_SYNC_DB,
    ) as should_proceed:
        if should_proceed:
            await repository.update(payload.id, MovieUpdateDB(**payload.model_dump()))
