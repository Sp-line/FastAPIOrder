from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from exceptions.db import (
    ObjectNotFoundException,
    UniqueFieldException,
    UniqueException,
    RelatedObjectNotFoundException,
    DeleteConstraintException,
    ExclusionException,
    CheckConstraintException
)


async def object_not_found_handler(_: Request, exc: ObjectNotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "object_id": exc.obj_id,
            "table_name": exc.table_name,
            "detail": str(exc),
        },
    )


async def unique_field_handler(_: Request, exc: UniqueFieldException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "field_name": exc.field_name,
            "table_name": exc.table_name,
            "detail": str(exc)
        },
    )


async def unique_handler(_: Request, exc: UniqueException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "fields": ", ".join(exc.fields),
            "table_name": exc.table_name,
            "detail": str(exc)
        },
    )


async def related_object_not_found_handler(_: Request, exc: RelatedObjectNotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "field_name": exc.field_name,
            "table_name": exc.table_name,
            "detail": str(exc)
        },
    )


async def delete_constraint_handler(_: Request, exc: DeleteConstraintException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "table_name": exc.table_name,
            "referencing_table": exc.referencing_table,
            "detail": str(exc)
        },
    )


async def exclusion_constraint_handler(_: Request, exc: ExclusionException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "fields": list(exc.fields),
            "table_name": exc.table_name,
            "detail": str(exc),
        }
    )


async def check_constraint_handler(_: Request, exc: CheckConstraintException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "table_name": exc.table_name,
            "failed_condition": exc.expression,
            "detail": str(exc),
        },
    )


async def integrity_error_handler(_: Request, exc: IntegrityError) -> JSONResponse:
    error_detail = str(exc.orig) if hasattr(exc, "orig") else str(exc)
    error_detail = error_detail.replace("\n", " ").strip()

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Database integrity error",
            "debug_message": error_detail,
        },
    )


def register_db_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ObjectNotFoundException, object_not_found_handler)  # type: ignore[arg-type]
    app.add_exception_handler(UniqueFieldException, unique_field_handler)  # type: ignore[arg-type]
    app.add_exception_handler(UniqueException, unique_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RelatedObjectNotFoundException, related_object_not_found_handler)  # type: ignore[arg-type]
    app.add_exception_handler(DeleteConstraintException, delete_constraint_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ExclusionException, exclusion_constraint_handler)  # type: ignore[arg-type]
    app.add_exception_handler(CheckConstraintException, check_constraint_handler)  # type: ignore[arg-type]
    app.add_exception_handler(IntegrityError, integrity_error_handler)  # type: ignore[arg-type]
