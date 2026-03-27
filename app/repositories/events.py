from types import TracebackType
from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from app_types import IntMap
from core.models.mixins.int_id_pk import IntIdPkMixin
from events import EventSession, Eventer
from .base import CommandRepositoryBase
from .unit_of_work import UnitOfWork
from repositories.integrity_handlers import TableErrorHandler
from schemas.base import Id
from schemas.events import CRUDEventSchemas


class EventCommandRepositoryBase[
    TModel: IntIdPkMixin,
    TCreateSchema: BaseModel,
    TUpdateSchema: BaseModel,
    TCreateEventSchema: BaseModel,
    TUpdateEventSchema: BaseModel,
    TDeleteEventSchema: Id,
](
    CommandRepositoryBase[
        TModel,
        TCreateSchema,
        TUpdateSchema,
        EventSession,
    ]
):
    def __init__(
            self,
            model: type[TModel],
            session: EventSession,
            table_error_handler: TableErrorHandler,
            eventer: Eventer,
            event_schemas: CRUDEventSchemas[
                TCreateEventSchema,
                TUpdateEventSchema,
                TDeleteEventSchema
            ]
    ) -> None:
        super().__init__(
            model=model,
            session=session,
            table_error_handler=table_error_handler
        )
        self._eventer = eventer
        self._event_schemas = event_schemas

    async def create(self, data: TCreateSchema) -> TModel:
        model = await super().create(data)
        self._session.events.append(
            self._eventer.create(self._event_schemas.create.model_validate(model))
        )
        return model

    async def bulk_create(self, data: list[TCreateSchema]) -> Sequence[TModel]:
        models = await super().bulk_create(data)
        self._session.events.append(
            self._eventer.bulk_create(
                [self._event_schemas.create.model_validate(model) for model in models],
            )
        )
        return models

    async def update(self, obj_id: int, obj: TUpdateSchema) -> TModel | None:
        model = await super().update(obj_id, obj)
        if model:
            self._session.events.append(
                self._eventer.update(
                    self._event_schemas.update.model_validate(model)
                )
            )
        return model

    async def bulk_update(self, data: IntMap[TUpdateSchema]) -> Sequence[TModel]:
        models = await super().bulk_update(data)
        self._session.events.append(
            self._eventer.bulk_update(
                [self._event_schemas.update.model_validate(model) for model in models],
            )
        )
        return models

    async def delete(self, obj_id: int) -> bool:
        stmt = (
            delete(self._model)
            .where(self._model.id == obj_id)
            .returning(self._model)
        )

        try:
            result = await self._session.execute(stmt)
            deleted_row = result.scalar_one_or_none()
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        if deleted_row:
            self._session.events.append(
                self._eventer.delete(
                    self._event_schemas.delete.model_validate(deleted_row)
                )
            )
            return True
        return False


class EventUnitOfWork[
    TSession: EventSession = EventSession
](
    UnitOfWork[
        TSession
    ]
):
    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        await super().__aexit__(
            exc_type,
            exc_val,
            exc_tb
        )
        if exc_type is None:
            await self._session.events.send_all()
