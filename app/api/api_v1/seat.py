from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from schemas.seat import SeatRead, SeatCreateReq, SeatUpdateReq
from service.seat import SeatService

router = APIRouter(route_class=DishkaRoute)


@router.get("/")
async def get_seats(service: FromDishka[SeatService], skip: int = 0, limit: int = 100) -> list[SeatRead]:
    return await service.get_all(skip, limit)


@router.get("/{seat_id}")
async def get_seat(seat_id: int, service: FromDishka[SeatService]) -> SeatRead:
    return await service.get_by_id(seat_id)


@router.post("/")
async def create_seat(data: SeatCreateReq, service: FromDishka[SeatService]) -> SeatRead:
    return await service.create(data)


@router.post("/bulk")
async def bulk_create_seats(data: list[SeatCreateReq], service: FromDishka[SeatService]) -> list[SeatRead]:
    return await service.bulk_create(data)


@router.patch("/{seat_id}")
async def update_seat(seat_id: int, data: SeatUpdateReq, service: FromDishka[SeatService]) -> SeatRead:
    return await service.update(seat_id, data)


@router.delete("/{seat_id}")
async def delete_seat(seat_id: int, service: FromDishka[SeatService]) -> None:
    return await service.delete(seat_id)
