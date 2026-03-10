from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from schemas.ticket import TicketRead
from service.ticket import TicketQueryService

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

