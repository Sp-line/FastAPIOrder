from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from constants import MovieLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Movie(IntIdPkMixin, Base):
    slug: Mapped[str] = mapped_column(String(MovieLimits.SLUG_MAX), unique=True)
    title: Mapped[str] = mapped_column(String(MovieLimits.TITLE_MAX))
