import uuid
from typing import Any

from sqlalchemy import String, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from constants import OutboxEventLimits
from core.models import Base
from core.models.mixins import IntIdPkMixin, ObservableMixin


class OutboxEvent(IntIdPkMixin, ObservableMixin, Base):
    code: Mapped[uuid.UUID] = mapped_column(
        UUID,
        default=uuid.uuid4,
        unique=True,
    )
    subject: Mapped[str] = mapped_column(String(OutboxEventLimits.SUBJECT_MAX))
    payload: Mapped[dict[str, Any] | list[Any]] = mapped_column(JSONB)
