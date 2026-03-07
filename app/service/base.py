from pydantic import BaseModel

from exceptions.db import ObjectNotFoundException
from repositories.base import RepositoryBase
from repositories.unit_of_work import UnitOfWork


class ServiceBase[
    TRepositoryBase: RepositoryBase,
    TReadSchema: BaseModel,
    TCreateSchema: BaseModel,
    TUpdateSchema: BaseModel,
    TDBCreateSchema: BaseModel,
    TDBUpdateSchema: BaseModel,
]:
    def __init__(
            self,
            repository: TRepositoryBase,
            unit_of_work: UnitOfWork,
            table_name: str,
            read_schema: type[TReadSchema],
            db_create_schema: type[TDBCreateSchema],
            db_update_schema: type[TDBUpdateSchema],
    ) -> None:
        self._repository = repository
        self._uof = unit_of_work
        self._table_name = table_name
        self._read_schema = read_schema
        self._db_create_schema = db_create_schema
        self._db_update_schema = db_update_schema

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[TReadSchema]:
        return [self._read_schema.model_validate(obj) for obj in await self._repository.get_all(skip, limit)]

    async def bulk_create(self, data: list[TCreateSchema]) -> list[TReadSchema]:
        bulk_create_data = self._bulk_create_data_transfer(data)
        async with self._uof:
            return [self._read_schema.model_validate(obj) for obj in await self._repository.bulk_create(bulk_create_data)]

    async def create(self, data: TCreateSchema) -> TReadSchema:
        create_data = self._create_data_transfer(data)
        async with self._uof:
            return self._read_schema.model_validate(await self._repository.create(create_data))

    async def get_by_id(self, obj_id: int) -> TReadSchema:
        if not (obj := await self._repository.get_by_id(obj_id)):
            raise ObjectNotFoundException(obj_id=obj_id, table_name=self._table_name)
        return self._read_schema.model_validate(obj)

    async def update(self, obj_id: int, data: TUpdateSchema) -> TReadSchema:
        update_data = self._update_data_transfer(data)
        async with self._uof:
            new_obj = await self._repository.update(obj_id, update_data)
            if not new_obj:
                raise ObjectNotFoundException(obj_id=obj_id, table_name=self._table_name)
            return self._read_schema.model_validate(new_obj)

    async def delete(self, obj_id: int) -> None:
        async with self._uof:
            if not await self._repository.delete(obj_id):
                raise ObjectNotFoundException(obj_id=obj_id, table_name=self._table_name)

    def _create_data_transfer(self, data: TCreateSchema) -> TDBCreateSchema:
        return self._db_create_schema.model_validate(data)

    def _bulk_create_data_transfer(self, data: list[TCreateSchema]) -> list[TDBCreateSchema]:
        return [self._db_create_schema.model_validate(obj) for obj in data]

    def _update_data_transfer(self, data: TUpdateSchema) -> TDBUpdateSchema:
        return self._db_update_schema(**data.model_dump(exclude_unset=True))
