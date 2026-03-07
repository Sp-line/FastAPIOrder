from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka
from dishka.integrations.taskiq import setup_dishka as setup_taskiq_dishka
from fastapi import FastAPI

from core import broker
from core.models import db_helper
from dependencies.infrastructure import InfrastructureProvider
from dependencies.repositories import RepositoryProvider
from dependencies.services import ServiceProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        await broker.startup()

    yield

    if not broker.is_worker_process:
        await broker.shutdown()
    await db_helper.dispose()


def create() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    container = make_async_container(
        InfrastructureProvider(),
        RepositoryProvider(),
        ServiceProvider()
    )

    setup_fastapi_dishka(container, app)
    setup_taskiq_dishka(container, broker)

    return app
