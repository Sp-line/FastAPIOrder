from typing import Annotated

from dishka.integrations.fastapi import (
    DishkaRoute,
    FromDishka,
)
from fastapi import APIRouter, Query

from schemas.base import Pagination
from schemas.order import OrderAdminRead
from schemas.ticket import (
    TicketCreateReq,
    TicketStatusUpdateReq,
    TicketPriceUpdateReq,
    TicketAdminRead
)
from services import TicketQueryService
from usage.ticket import (
    AddTicketToOrderUsage,
    RemoveTicketFromOrderUsage,
    AddTicketsToOrdersUsage,
    UpdateTicketStatusInOrderUsage,
    UpdateTicketPriceInOrderUsage
)

router = APIRouter(route_class=DishkaRoute)


@router.get("/", summary="[Admin] Get Tickets")
async def get_tickets(
        service: FromDishka[TicketQueryService],
        query: Annotated[Pagination, Query()]
) -> list[TicketAdminRead]:
    return await service.get_all(query.skip, query.limit)


@router.get("/{ticket_id}", summary="[Admin] Get Ticket")
async def get_ticket(ticket_id: int, service: FromDishka[TicketQueryService]) -> TicketAdminRead:
    return await service.get_by_id(ticket_id)


@router.post("/", summary="[Admin] Create Ticket")
async def create_ticket(
        data: TicketCreateReq,
        add_ticket_to_order_usage: FromDishka[AddTicketToOrderUsage]
) -> TicketAdminRead:
    return await add_ticket_to_order_usage(data)


@router.post("/bulk", summary="[Admin] Bulk Create Ticket")
async def bulk_create_tickets(
        add_tickets_to_orders_usage: FromDishka[AddTicketsToOrdersUsage],
        data: list[TicketCreateReq],
) -> list[TicketAdminRead]:
    return await add_tickets_to_orders_usage(data)


@router.delete("/{ticket_id}", summary="[Admin] Delete Ticket")
async def delete_ticket(
        ticket_id: int,
        remove_ticket_from_order_usage: FromDishka[RemoveTicketFromOrderUsage]
) -> OrderAdminRead:
    return await remove_ticket_from_order_usage(ticket_id)


@router.put("/status/{ticket_id}", summary="[Admin] Update Ticket Status")
async def update_ticket_status(
        ticket_id: int,
        data: TicketStatusUpdateReq,
        update_ticket_status_in_order_usage: FromDishka[UpdateTicketStatusInOrderUsage],
) -> TicketAdminRead:
    return await update_ticket_status_in_order_usage(ticket_id, data)


@router.put("/price/{ticket_id}", summary="[Admin] Update Ticket Price")
async def update_ticket_price(
        ticket_id: int,
        data: TicketPriceUpdateReq,
        update_ticket_price_in_order_usage: FromDishka[UpdateTicketPriceInOrderUsage],
) -> TicketAdminRead:
    return await update_ticket_price_in_order_usage(ticket_id, data)
