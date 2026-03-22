from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from schemas.order import OrderRead
from schemas.ticket import TicketRead, TicketCreateReq
from services.ticket import TicketQueryService
from usage.ticket import AddTicketToOrderUsage, RemoveTicketFromOrderUsage

router = APIRouter(route_class=DishkaRoute)


@router.get("/", summary="[Admin] Get Tickets")
async def get_tickets(service: FromDishka[TicketQueryService], skip: int = 0, limit: int = 100) -> list[TicketRead]:
    return await service.get_all(skip, limit)


@router.get("/{ticket_id}", summary="[Admin] Get Ticket")
async def get_ticket(ticket_id: int, service: FromDishka[TicketQueryService]) -> TicketRead:
    return await service.get_by_id(ticket_id)


@router.get("/public/{public_code}")
async def get_ticket_by_public_code(public_code: UUID, service: FromDishka[TicketQueryService]) -> TicketRead:
    return await service.get_by_public_code(public_code)


@router.get("/list/{user_id}")
async def get_tickets_by_user_id(user_id: int, service: FromDishka[TicketQueryService]) -> list[TicketRead]:
    return await service.get_by_user_id(user_id)


@router.post("/", summary="[Admin] Create Ticket")
async def create_ticket(data: TicketCreateReq, add_ticket_to_order_usage: FromDishka[AddTicketToOrderUsage]) -> TicketRead:
    return await add_ticket_to_order_usage(data)


@router.delete("/{ticket_id}", summary="[Admin] Delete Ticket")
async def delete_ticket(ticket_id: int, remove_ticket_from_order_usage: FromDishka[RemoveTicketFromOrderUsage]) -> OrderRead:
    return await remove_ticket_from_order_usage(ticket_id)
