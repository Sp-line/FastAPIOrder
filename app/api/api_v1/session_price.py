from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from schemas.session_price import SessionPriceRead, SessionPriceCreateReq, SessionPriceUpdateReq
from service.session_price import SessionPriceService

router = APIRouter(route_class=DishkaRoute)


@router.get("/")
async def get_session_prices(service: FromDishka[SessionPriceService], skip: int = 0, limit: int = 100) -> list[SessionPriceRead]:
    return await service.get_all(skip, limit)


@router.get("/{session_price_id}")
async def get_session_price(session_price_id: int, service: FromDishka[SessionPriceService]) -> SessionPriceRead:
    return await service.get_by_id(session_price_id)


@router.post("/", summary="[Admin] Create SessionPrice")
async def create_session_price(data: SessionPriceCreateReq, service: FromDishka[SessionPriceService]) -> SessionPriceRead:
    return await service.create(data)


@router.post("/bulk", summary="[Admin] Bulk Create SessionPrice")
async def bulk_create_session_prices(data: list[SessionPriceCreateReq], service: FromDishka[SessionPriceService]) -> list[SessionPriceRead]:
    return await service.bulk_create(data)


@router.patch("/{session_price_id}", summary="[Admin] Update SessionPrice")
async def update_session_price(session_price_id: int, data: SessionPriceUpdateReq, service: FromDishka[SessionPriceService]) -> SessionPriceRead:
    return await service.update(session_price_id, data)


@router.delete("/{session_price_id}", summary="[Admin] Delete SessionPrice")
async def delete_session_price(session_price_id: int, service: FromDishka[SessionPriceService]) -> None:
    return await service.delete(session_price_id)
