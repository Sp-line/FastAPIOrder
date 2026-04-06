import uuid

from sqlalchemy import UUID, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from constants import InboxEventLimits
from core.models import Base
from core.models.mixins import IntIdPkMixin, ObservableMixin


class InboxEvent(IntIdPkMixin, ObservableMixin, Base):
    code: Mapped[uuid.UUID] = mapped_column(UUID)
    handler: Mapped[str] = mapped_column(String(InboxEventLimits.HANDLER_MAX))

    __table_args__ = (
        UniqueConstraint("code", "handler", name="uq_inbox_events_code_handler"),
    )
