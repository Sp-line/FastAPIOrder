from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.mixins.int_id_pk import IntIdPkMixin
from integrity_handlers.base import TableErrorHandler


class QueryRepositoryBase[
    TModel: IntIdPkMixin,
    TSession: AsyncSession = AsyncSession,
]:
    def __init__(self, model: type[TModel], session: TSession) -> None:
        self._model = model
        self._session = session

    async def get_by_ids(self, obj_ids: list[int]) -> Sequence[TModel]:
        if not obj_ids:
            return []

        stmt = select(self._model).where(self._model.id.in_(obj_ids))
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[TModel]:
        stmt = select(self._model).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, obj_id: int) -> TModel | None:
        return await self._session.get(self._model, obj_id)


class CommandRepositoryBase[
    TModel: IntIdPkMixin,
    TCreateSchema: BaseModel,
    TUpdateSchema: BaseModel,
    TSession: AsyncSession = AsyncSession,
]:
    def __init__(
            self,
            model: type[TModel],
            session: TSession,
            table_error_handler: TableErrorHandler
    ) -> None:
        self._model = model
        self._session = session
        self._table_error_handler = table_error_handler

    async def create(self, data: TCreateSchema) -> TModel:
        obj = self._model(**data.model_dump())
        self._session.add(obj)

        try:
            await self._session.flush()
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        await self._session.refresh(obj)
        return obj

    async def bulk_create(self, data: list[TCreateSchema]) -> list[TModel]:
        if not data:
            return []

        objs = [self._model(**item.model_dump()) for item in data]
        self._session.add_all(objs)

        try:
            await self._session.flush()
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        return objs

    async def update(self, obj_id: int, data: TUpdateSchema) -> TModel | None:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return await self._session.get(self._model, obj_id)

        stmt = (
            update(self._model)
            .where(self._model.id == obj_id)
            .values(**update_data)
            .returning(self._model)
        )

        try:
            result = await self._session.execute(stmt)
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        return result.scalar_one_or_none()

    async def delete(self, obj_id: int) -> bool:
        stmt = delete(self._model).where(self._model.id == obj_id)

        try:
            result = await self._session.execute(stmt)
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        return result.rowcount > 0  # type: ignore


class RepositoryBase[
    TModel: IntIdPkMixin,
    TCreateSchema: BaseModel,
    TUpdateSchema: BaseModel,
    TSession: AsyncSession = AsyncSession,
](
    QueryRepositoryBase[TModel, TSession],
    CommandRepositoryBase[TModel, TCreateSchema, TUpdateSchema, TSession]
):
    def __init__(
            self,
            model: type[TModel],
            session: TSession,
            table_error_handler: TableErrorHandler
    ) -> None:
        QueryRepositoryBase.__init__(
            self,
            model=model,
            session=session
        )
        CommandRepositoryBase.__init__(
            self,
            model=model,
            session=session,
            table_error_handler=table_error_handler
        )
