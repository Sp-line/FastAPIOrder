from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from schemas.user import UserRead, UserCreateReq, UserUpdateReq
from services.user import UserService

router = APIRouter(route_class=DishkaRoute)


@router.get("/")
async def get_users(service: FromDishka[UserService], skip: int = 0, limit: int = 100) -> list[UserRead]:
    return await service.get_all(skip, limit)


@router.get("/{user_id}")
async def get_user(user_id: int, service: FromDishka[UserService]) -> UserRead:
    return await service.get_by_id(user_id)


@router.post("/", summary="[Admin] Create User")
async def create_user(data: UserCreateReq, service: FromDishka[UserService]) -> UserRead:
    return await service.create(data)


@router.post("/bulk", summary="[Admin] Bulk Create User")
async def bulk_create_users(data: list[UserCreateReq], service: FromDishka[UserService]) -> list[UserRead]:
    return await service.bulk_create(data)


@router.patch("/{user_id}", summary="[Admin] Update User")
async def update_user(user_id: int, data: UserUpdateReq, service: FromDishka[UserService]) -> UserRead:
    return await service.update(user_id, data)


@router.delete("/{user_id}", summary="[Admin] Delete User")
async def delete_user(user_id: int, service: FromDishka[UserService]) -> None:
    return await service.delete(user_id)
