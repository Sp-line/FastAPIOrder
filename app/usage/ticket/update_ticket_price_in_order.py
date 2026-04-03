from repositories import (
    TicketRepository,
    OrderRepository,
    UnitOfWork
)
from schemas.order import OrderUpdateDB
from schemas.ticket import (
    TicketPriceUpdateReq,
    TicketUpdateDB,
    TicketAdminRead
)
from services.booking import PricingStrategy
from usage.ticket.facades import (
    UpdateTicketPriceInOrderDomain,
    UpdateTicketPriceInOrderDataExistenceServices
)


class UpdateTicketPriceInOrderUsage:
    def __init__(
            self,
            ticket_repo: TicketRepository,
            order_repo: OrderRepository,
            unit_of_work: UnitOfWork,

            domain: UpdateTicketPriceInOrderDomain,
            data_existence: UpdateTicketPriceInOrderDataExistenceServices,
            pricing: PricingStrategy,
    ) -> None:
        self._ticket_repo = ticket_repo
        self._order_repo = order_repo
        self._uow = unit_of_work

        self._domain = domain
        self._data_existence = data_existence
        self._pricing = pricing

    async def __call__(self, ticket_id: int, data: TicketPriceUpdateReq) -> TicketAdminRead:
        ticket = self._data_existence.ticket.ensure_obj_exist(
            obj_id=ticket_id,
            obj=await self._ticket_repo.get_by_id(ticket_id)
        )

        if ticket.price == data.price:
            return TicketAdminRead.model_validate(ticket)

        order = self._data_existence.order.ensure_obj_exist(
            obj_id=ticket.order_id,
            obj=await self._order_repo.get_by_id(ticket.order_id)
        )

        self._domain.ticket_is_reserved_for_price_change(ticket_status=ticket.status)
        self._domain.order_is_pending_for_price_change(order_status=order.status)

        new_order_total_price = self._pricing.update_ticket_price(
            order_total=order.total_price,
            old_price=ticket.price,
            new_price=data.price
        )

        async with self._uow:
            updated_ticket = await self._ticket_repo.update(
                obj_id=ticket.id,
                data=TicketUpdateDB(
                    price=data.price
                )
            )

            await self._order_repo.update(
                obj_id=order.id,
                data=OrderUpdateDB(
                    total_price=new_order_total_price
                )
            )

            return TicketAdminRead.model_validate(updated_ticket)
