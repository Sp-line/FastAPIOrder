from dishka.integrations.faststream import FromDishka
from faststream import AckPolicy
from pydantic import TypeAdapter

from core import (
    fs_router,
    catalog_stream
)
from handlers.base import base_consumer_config
from repositories.movie import MovieRepository
from repositories.unit_of_work import UnitOfWork
from schemas.movie import (
    MovieCreateEvent,
    MovieCreateDB,
    MovieUpdateEvent,
    MovieUpdateDB
)


@fs_router.subscriber(
    "catalog.movies.created",
    stream=catalog_stream,
    durable="movie_svc_movies_created_sync_db",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def movies_created_on_movie_microservice_sync_db(
        payload: MovieCreateEvent,
        repository: FromDishka[MovieRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.create(MovieCreateDB(**payload.model_dump()))


@fs_router.subscriber(
    "catalog.movies.bulk.created",
    stream=catalog_stream,
    durable="movie_svc_movies_bulk_created_sync_db",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def movies_bulk_created_on_movie_microservice_sync_db(
        payload: list[MovieCreateEvent],
        repository: FromDishka[MovieRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.bulk_create(
            TypeAdapter(list[MovieCreateDB]).validate_python(payload),
        )


@fs_router.subscriber(
    "catalog.movies.updated",
    stream=catalog_stream,
    durable="movie_svc_movies_updated_sync_db",
    ack_policy=AckPolicy.NACK_ON_ERROR,
    config=base_consumer_config
)
async def movies_updated_on_movie_microservice_sync_db(
        payload: MovieUpdateEvent,
        repository: FromDishka[MovieRepository],
        unit_of_work: FromDishka[UnitOfWork],
) -> None:
    async with unit_of_work:
        await repository.update(payload.id, MovieUpdateDB(**payload.model_dump()))
