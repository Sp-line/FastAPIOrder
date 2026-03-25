import asyncio
import uuid
from decimal import Decimal

from pydantic import TypeAdapter

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
from services.booking import (
    OrderSchedulerService,
)
from usage.order.facades import BulkCreateOrderDataExistenceServices
from utils import (
    get_ids,
    build_map
)


class BulkCreateOrderUsage:
    def __init__(
            self,
            order_repo: OrderRepository,
            user_repo: UserRepository,
            unit_of_work: UnitOfWork,

            scheduler: OrderSchedulerService,
            data_existence: BulkCreateOrderDataExistenceServices,
    ) -> None:
        self._order_repo = order_repo
        self._user_repo = user_repo
        self._uow = unit_of_work

        self._scheduler = scheduler
        self._data_existence = data_existence

    async def __call__(self, data: list[OrderCreateReq]) -> list[OrderRead]:
        if not data:
            return []

        user_ids = get_ids(data, "user_id")
        users = await self._user_repo.get_by_ids(user_ids)
        users_map = build_map(users)
        self._data_existence.user.ensure_objs_exist(
            data=data,
            obj_id_field="user_id",
            objs_map=users_map
        )

        orders_create_data: list[OrderCreateDB] = []

        for item in data:
            schedule_id = str(uuid.uuid4())

            orders_create_data.append(
                OrderCreateDB(  # type: ignore[call-arg]
                    user_id=item.user_id,
                    total_price=Decimal("0.00"),
                    expires_at=item.expires_at,
                    expire_schedule_id=schedule_id,
                    status=OrderStatus.PENDING
                )
            )

        adapter = TypeAdapter(list[OrderRead])

        async with self._uow:
            created_orders = await self._order_repo.bulk_create(orders_create_data)

            scheduling_coroutines = [
                self._scheduler.schedule_expiration(
                    schedule_id=order.expire_schedule_id,
                    expires_at=order.expires_at,
                    order_id=order.id
                )
                for order in created_orders
                if order.expire_schedule_id
            ]

            if scheduling_coroutines:
                await asyncio.gather(*scheduling_coroutines)

            return adapter.validate_python(created_orders)
