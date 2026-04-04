import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins import IntIdPkMixin, ObservableMixin


class InboxEvent(IntIdPkMixin, ObservableMixin, Base):
    code: Mapped[uuid.UUID] = mapped_column(UUID, unique=True)
