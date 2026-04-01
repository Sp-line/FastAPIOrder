from typing import Annotated

from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka
)
from fastapi import APIRouter, Query

from schemas.base import Pagination
from schemas.session import (
    SessionRead,
    SessionUpdateReq,
    SessionCreateReq,
)
from services import SessionService

router = APIRouter(route_class=DishkaRoute)


@router.get("/")
async def get_sessions(
        service: FromDishka[SessionService],
        query: Annotated[Pagination, Query()]
) -> list[SessionRead]:
    return await service.get_all(query.skip, query.limit)


@router.get("/{session_id}")
async def get_session(session_id: int, service: FromDishka[SessionService]) -> SessionRead:
    return await service.get_by_id(session_id)


@router.post("/", summary="[Admin] Create Session")
async def create_session(data: SessionCreateReq, service: FromDishka[SessionService]) -> SessionRead:
    return await service.create(data)


@router.post("/bulk", summary="[Admin] Bulk Create Session")
async def bulk_create_sessions(data: list[SessionCreateReq], service: FromDishka[SessionService]) -> list[SessionRead]:
    return await service.bulk_create(data)


@router.patch("/{session_id}", summary="[Admin] Update Session")
async def update_session(session_id: int, data: SessionUpdateReq, service: FromDishka[SessionService]) -> SessionRead:
    return await service.update(session_id, data)


@router.delete("/{session_id}", summary="[Admin] Delete Session")
async def delete_session(session_id: int, service: FromDishka[SessionService]) -> None:
    return await service.delete(session_id)
