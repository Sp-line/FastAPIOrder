from fastapi import FastAPI

from exceptions.handlers.db import register_db_exception_handlers


def register_exception_handlers(app: FastAPI) -> None:
    register_db_exception_handlers(app)
