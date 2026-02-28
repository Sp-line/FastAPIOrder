from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from constants import UserLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class User(IntIdPkMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    email: Mapped[str] = mapped_column(String(UserLimits.EMAIL_MAX), unique=True)
    first_name: Mapped[str] = mapped_column(String(UserLimits.FIRST_NAME_MAX))
    last_name: Mapped[str] = mapped_column(String(UserLimits.LAST_NAME_MAX))
    phone_number: Mapped[str | None] = mapped_column(String(UserLimits.PHONE_MAX), unique=True)
