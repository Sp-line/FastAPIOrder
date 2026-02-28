from decimal import Decimal
from typing import TYPE_CHECKING

from utils import generate_order_public_code

if TYPE_CHECKING:
    from core.models import User

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Uuid, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import OrderLimits, OrderStatus
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import User, Ticket


class Order(IntIdPkMixin, Base):
    number: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), default=uuid4, unique=True)
    public_code: Mapped[str] = mapped_column(String(OrderLimits.PUBLIC_CODE_MAX), default=generate_order_public_code, unique=True)
    status: Mapped[str] = mapped_column(String(OrderLimits.STATUS_MAX), default=OrderStatus.PENDING.value, index=True)

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    expire_schedule_id: Mapped[str | None] = mapped_column(String(OrderLimits.EXPIRE_SCHEDULE_ID_MAX), unique=True)

    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)

    user: Mapped["User"] = relationship(back_populates="orders")

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="order", cascade="all, delete-orphan")
