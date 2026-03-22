from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)
from fastapi import APIRouter

from schemas.order import OrderAdminRead
from services import OrderQueryService

router = APIRouter(route_class=DishkaRoute)


@router.get("/", summary="[Admin] Get Orders")
async def get_orders(service: FromDishka[OrderQueryService], skip: int = 0, limit: int = 100) -> list[OrderAdminRead]:
    return await service.get_all(skip, limit)


@router.get("/{order_id}", summary="[Admin] Get Order")
async def get_order(order_id: int, service: FromDishka[OrderQueryService]) -> OrderAdminRead:
    return await service.get_by_id(order_id)
