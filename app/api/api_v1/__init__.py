from fastapi import APIRouter

from core.config import settings
from .hall import router as hall_router
from .session import router as session_router
from .movie import router as movie_router
from .user import router as user_router
from .seat import router as seat_router
from .booking import router as booking_router
from .ticket import router as ticket_router
from .session_price import router as session_price_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(hall_router, prefix="/halls", tags=["Halls"])
router.include_router(session_router, prefix="/sessions", tags=["Sessions"])
router.include_router(movie_router, prefix="/movies", tags=["Movies"])
router.include_router(seat_router, prefix="/seats", tags=["Seats"])
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(ticket_router, prefix="/tickets", tags=["Tickets"])
router.include_router(booking_router, prefix="/bookings", tags=["Bookings"])
router.include_router(session_price_router, prefix="/session-prices", tags=["Session-Prices"])
