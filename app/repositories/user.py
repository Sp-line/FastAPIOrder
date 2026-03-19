from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from repositories.integrity_handlers import user_error_handler
from repositories.base import RepositoryBase
from schemas.user import UserCreateDB, UserUpdateDB


class UserRepository(
    RepositoryBase[
        User,
        UserCreateDB,
        UserUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=User,
            session=session,
            table_error_handler=user_error_handler,
        )
