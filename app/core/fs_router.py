import logging

from fastapi import FastAPI
from faststream.nats import JStream
from faststream.nats.fastapi import NatsRouter

from core.config import settings

router = NatsRouter(str(settings.faststream.nats_url))

catalog_stream = JStream(name="catalog_stream", declare=False)

showtimes_stream = JStream("showtimes_stream", declare=False)


@router.after_startup
async def configure_logging(app: FastAPI) -> None:
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.log_format,
        datefmt=settings.logging.log_datefmt,
    )
