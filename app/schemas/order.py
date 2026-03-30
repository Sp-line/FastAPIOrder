from datetime import datetime, timezone, timedelta
from decimal import Decimal
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, PositiveInt, ConfigDict

from constants import OrderStatus, OrderLimits
from schemas.base import Id
from schemas.events import CRUDEventSchemas
from utils import generate_order_public_code


class OrderBase(BaseModel):
    pass


class OrderBaseWithRelations(OrderBase):
    user_id: PositiveInt


class OrderCreateReq(OrderBaseWithRelations):
    expires_at: Annotated[datetime, Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(minutes=OrderLimits.EXPIRE_MINUTES))]


class OrderCreateDB(OrderCreateReq):
    number: Annotated[UUID, Field(default_factory=uuid4)]
    public_code: Annotated[str, Field(max_length=OrderLimits.PUBLIC_CODE_MAX, default_factory=generate_order_public_code)]

    status: Annotated[OrderStatus, Field(default=OrderStatus.PENDING)]
    expire_schedule_id: Annotated[str | None, Field(max_length=OrderLimits.EXPIRE_SCHEDULE_ID_MAX)]
    total_price: Annotated[Decimal, Field(ge=OrderLimits.TOTAL_PRICE_MIN)]


class OrderUpdateBase(BaseModel):
    pass


class OrderUpdateReq(OrderUpdateBase):
    pass


class OrderUpdateDB(OrderUpdateReq):
    number: UUID | None = None
    public_code: Annotated[str | None, Field(max_length=OrderLimits.PUBLIC_CODE_MAX)] = None

    status: OrderStatus | None = None
    expires_at: datetime | None = None
    expire_schedule_id: Annotated[str | None, Field(max_length=OrderLimits.EXPIRE_SCHEDULE_ID_MAX)] = None
    total_price: Annotated[Decimal | None, Field(ge=OrderLimits.TOTAL_PRICE_MIN)] = None

    user_id: PositiveInt | None = None


class OrderRead(OrderBaseWithRelations):
    number: UUID
    public_code: Annotated[str, Field(max_length=OrderLimits.PUBLIC_CODE_MAX)]

    status: OrderStatus
    expires_at: datetime
    total_price: Annotated[Decimal, Field(ge=OrderLimits.TOTAL_PRICE_MIN)]

    model_config = ConfigDict(from_attributes=True)


class OrderAdminRead(Id, OrderRead):
    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdateReq(BaseModel):
    status: OrderStatus


class OrderCreateEvent(OrderAdminRead):
    model_config = ConfigDict(extra='ignore')


class OrderUpdateEvent(OrderAdminRead):
    model_config = ConfigDict(extra='ignore')


order_event_schemas = CRUDEventSchemas[
    OrderCreateEvent,
    OrderUpdateEvent,
    Id
](
    create=OrderCreateEvent,
    update=OrderUpdateEvent,
    delete=Id
)
