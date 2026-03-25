import uuid
from decimal import Decimal

from constants import OrderStatus
from repositories import (
    OrderRepository,
    UserRepository,
    UnitOfWork
)
from schemas.order import (
    OrderCreateReq,
    OrderRead,
    OrderCreateDB
)
from services import TaskScheduler
from tasks.order import set_unpaid_order_with_tickets_as_expired
from usage.order.facades import CreateOrderDataExistenceServices


class OrderCreateUsage:
    def __init__(
            self,
            order_repo: OrderRepository,
            user_repo: UserRepository,
            unit_of_work: UnitOfWork,

            scheduler: TaskScheduler,
            data_existence: CreateOrderDataExistenceServices,
    ) -> None:
        self._order_repo = order_repo
        self._user_repo = user_repo
        self._uow = unit_of_work

        self._scheduler = scheduler
        self._data_existence = data_existence

    async def __call__(self, data: OrderCreateReq) -> OrderRead:
        user = self._data_existence.user.ensure_obj_exist(
            obj_id=data.user_id,
            obj=await self._user_repo.get_by_id(data.user_id)
        )

        schedule_id = str(uuid.uuid4())

        async with self._uow:
            order_create_data = OrderCreateDB(  # type: ignore[call-arg]
                user_id=user.id,
                total_price=Decimal("0.00"),
                expires_at=data.expires_at,
                expire_schedule_id=schedule_id,
                status=OrderStatus.PENDING
            )

            order = await self._order_repo.create(order_create_data)

            await self._scheduler.schedule_by_time(  # type: ignore[call-arg]
                task=set_unpaid_order_with_tickets_as_expired,
                schedule_id=schedule_id,
                expires_at=data.expires_at,
                order_id=order.id,
            )

            return OrderRead.model_validate(order)
