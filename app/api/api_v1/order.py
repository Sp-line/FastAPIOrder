from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)
from fastapi import APIRouter

from schemas.order import (
    OrderAdminRead,
    OrderCreateReq,
    OrderStatusUpdateReq
)
from services import OrderQueryService
from usage.order import (
    OrderCreateUsage,
    BulkCreateOrderUsage,
    UpdateOrderStatusUsage,
    OrderDeleteUsage
)

router = APIRouter(route_class=DishkaRoute)


@router.get("/", summary="[Admin] Get Orders")
async def get_orders(service: FromDishka[OrderQueryService], skip: int = 0, limit: int = 100) -> list[OrderAdminRead]:
    return await service.get_all(skip, limit)


@router.get("/{order_id}", summary="[Admin] Get Order")
async def get_order(order_id: int, service: FromDishka[OrderQueryService]) -> OrderAdminRead:
    return await service.get_by_id(order_id)


@router.post("/", summary="[Admin] Create Order")
async def create_order(
        create_order_usage: FromDishka[OrderCreateUsage],
        data: OrderCreateReq
) -> OrderAdminRead:
    return await create_order_usage(data)


@router.post("/bulk", summary="[Admin] Bulk Create Order")
async def bulk_create_orders(
        data: list[OrderCreateReq],
        bulk_create_order_usage: FromDishka[BulkCreateOrderUsage]
) -> list[OrderAdminRead]:
    return await bulk_create_order_usage(data)


@router.put("/status/{order_id}", summary="[Admin] Update Order Status")
async def update_order_status(
        order_id: int,
        data: OrderStatusUpdateReq,
        update_order_status_usage: FromDishka[UpdateOrderStatusUsage],
) -> OrderAdminRead:
    return await update_order_status_usage(order_id, data)


@router.delete("/{order_id}", summary="[Admin] Delete Order")
async def delete_order(
        order_id: int,
        order_delete_usage: FromDishka[OrderDeleteUsage]
) -> None:
    return await order_delete_usage(order_id)
