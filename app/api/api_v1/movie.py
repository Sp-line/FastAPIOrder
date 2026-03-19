from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from schemas.movie import MovieRead, MovieCreateReq, MovieUpdateReq
from services.movie import MovieService

router = APIRouter(route_class=DishkaRoute)


@router.get("/")
async def get_movies(service: FromDishka[MovieService], skip: int = 0, limit: int = 100) -> list[MovieRead]:
    return await service.get_all(skip, limit)


@router.get("/{movie_id}")
async def get_movie(movie_id: int, service: FromDishka[MovieService]) -> MovieRead:
    return await service.get_by_id(movie_id)


@router.post("/", summary="[Admin] Create Movie")
async def create_movie(data: MovieCreateReq, service: FromDishka[MovieService]) -> MovieRead:
    return await service.create(data)


@router.post("/bulk", summary="[Admin] Bulk Create Movie")
async def bulk_create_movies(data: list[MovieCreateReq], service: FromDishka[MovieService]) -> list[MovieRead]:
    return await service.bulk_create(data)


@router.patch("/{movie_id}", summary="[Admin] Update Movie")
async def update_movie(movie_id: int, data: MovieUpdateReq, service: FromDishka[MovieService]) -> MovieRead:
    return await service.update(movie_id, data)


@router.delete("/{movie_id}", summary="[Admin] Delete Movie")
async def delete_movie(movie_id: int, service: FromDishka[MovieService]) -> None:
    return await service.delete(movie_id)
