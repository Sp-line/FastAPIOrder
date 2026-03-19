from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from schemas.booking import BookingOrderRead
from usage.booking import GetBookingByNumberUsage

router = APIRouter(route_class=DishkaRoute)


@router.get("/{order_number}", summary="Get Booking")
async def get_booking(order_number: UUID, get_booking_usage: FromDishka[GetBookingByNumberUsage]) -> BookingOrderRead:
    return await get_booking_usage(order_number)
