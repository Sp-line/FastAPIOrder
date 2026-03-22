from repositories import (
    UnitOfWork,
    UserRepository
)
from schemas.user import (
    UserRead,
    UserCreateReq,
    UserUpdateReq,
    UserCreateDB,
    UserUpdateDB
)
from services import ServiceBase


class UserService(
    ServiceBase[
        UserRepository,
        UserRead,
        UserCreateReq,
        UserUpdateReq,
        UserCreateDB,
        UserUpdateDB,
    ],
):
    def __init__(self, repository: UserRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="users",
            read_schema=UserRead,
            db_create_schema=UserCreateDB,
            db_update_schema=UserUpdateDB,
        )
