import logging

import taskiq_fastapi
from taskiq import TaskiqEvents, TaskiqState, TaskiqScheduler
from taskiq_redis import ListQueueBroker, ListRedisScheduleSource

from .config import settings

log = logging.getLogger(__name__)

broker = ListQueueBroker(url=str(settings.taskiq.url))
redis_source = ListRedisScheduleSource(str(settings.taskiq.url))
scheduler = TaskiqScheduler(broker, sources=[redis_source])

taskiq_fastapi.init(broker, "main:main_app")


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.taskiq.log_format,
        datefmt=settings.logging.log_datefmt,
    )
    log.info(f"Worker startup complete, got state: %s", state)
