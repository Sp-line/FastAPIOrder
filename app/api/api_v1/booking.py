from uuid import UUID

from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)
from fastapi import APIRouter

from schemas.booking import (
    BookingOrderRead,
    BookingOrderCreateReq,
)
from usage.booking import (
    GetBookingByNumberUsage,
    GetBookingsByUserIDUsage,
    CreateBookingUsage,
)

router = APIRouter(route_class=DishkaRoute)


@router.post("/orders", summary="Create Booking")
async def create_booking(
        data: BookingOrderCreateReq,
        create_booking_usage: FromDishka[CreateBookingUsage]
) -> BookingOrderRead:
    return await create_booking_usage(data)


@router.get("/orders/{order_number}", summary="Get Booking")
async def get_booking(
        order_number: UUID,
        get_booking_usage: FromDishka[GetBookingByNumberUsage]
) -> BookingOrderRead:
    return await get_booking_usage(order_number)


@router.get("/orders/users/{user_id}", summary="Get Bookings")
async def get_bookings_by_user_id(
        get_bookings_by_user_id_usage: FromDishka[GetBookingsByUserIDUsage],
        user_id: int,
        skip: int = 0,
        limit: int = 100,
) -> list[BookingOrderRead]:
    return await get_bookings_by_user_id_usage(user_id, skip, limit)
