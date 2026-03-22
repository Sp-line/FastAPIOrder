from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)
from fastapi import APIRouter

from schemas.hall import (
    HallRead,
    HallCreateReq,
    HallUpdateReq
)
from services import HallService

router = APIRouter(route_class=DishkaRoute)


@router.get("/")
async def get_halls(service: FromDishka[HallService], skip: int = 0, limit: int = 100) -> list[HallRead]:
    return await service.get_all(skip, limit)


@router.get("/{hall_id}")
async def get_hall(hall_id: int, service: FromDishka[HallService]) -> HallRead:
    return await service.get_by_id(hall_id)


@router.post("/", summary="[Admin] Create Hall")
async def create_hall(data: HallCreateReq, service: FromDishka[HallService]) -> HallRead:
    return await service.create(data)


@router.post("/bulk", summary="[Admin] Bulk Create Hall")
async def bulk_create_halls(data: list[HallCreateReq], service: FromDishka[HallService]) -> list[HallRead]:
    return await service.bulk_create(data)


@router.patch("/{hall_id}", summary="[Admin] Update Hall")
async def update_hall(hall_id: int, data: HallUpdateReq, service: FromDishka[HallService]) -> HallRead:
    return await service.update(hall_id, data)


@router.delete("/{hall_id}", summary="[Admin] Delete Hall")
async def delete_hall(hall_id: int, service: FromDishka[HallService]) -> None:
    return await service.delete(hall_id)
