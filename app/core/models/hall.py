from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from constants import HallLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Hall(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(HallLimits.NAME_MAX))
    slug: Mapped[str] = mapped_column(String(HallLimits.SLUG_MAX), unique=True)
