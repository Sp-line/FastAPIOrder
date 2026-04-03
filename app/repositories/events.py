from collections.abc import Iterable
from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app_types import IntMap
from core.config import settings
from core.models import OutboxEvent
from core.models.mixins import IntIdPkMixin
from events.topics import CRUDTopics
from repositories.integrity_handlers import TableErrorHandler
from schemas.base import Id
from schemas.events import CRUDEventSchemas
from .base import CommandRepositoryBase


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
        AsyncSession,
    ]
):
    def __init__(
            self,
            model: type[TModel],
            session: AsyncSession,
            table_error_handler: TableErrorHandler,
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
        self._event_schemas = event_schemas
        self._topics = CRUDTopics.generate(
            microservice=settings.faststream.microservice,
            table_name=self._model.__tablename__  # type: ignore[attr-defined]
        )

    async def create(self, data: TCreateSchema) -> TModel:
        model = await super().create(data)
        payload = self._event_schemas.create.model_validate(model).model_dump(mode="json")

        outbox_event = OutboxEvent(
            subject=self._topics.create,
            payload=payload,
        )
        self._session.add(outbox_event)

        return model

    async def bulk_create(self, data: Iterable[TCreateSchema]) -> Sequence[TModel]:
        models = await super().bulk_create(data)
        if models:
            payloads = [
                self._event_schemas.create.model_validate(model).model_dump(mode="json")
                for model in models
            ]

            outbox_event = OutboxEvent(
                subject=self._topics.bulk_create,
                payload=payloads,
            )
            self._session.add(outbox_event)

        return models

    async def update(self, obj_id: int, data: TUpdateSchema) -> TModel | None:
        model = await super().update(obj_id, data)
        if model:
            payload = self._event_schemas.update.model_validate(model).model_dump(mode="json")
            outbox_event = OutboxEvent(
                subject=self._topics.update,
                payload=payload,
            )
            self._session.add(outbox_event)

        return model

    async def bulk_update(self, data: IntMap[TUpdateSchema]) -> Sequence[TModel]:
        models = await super().bulk_update(data)
        if models:
            payloads = [
                self._event_schemas.update.model_validate(model).model_dump(mode="json")
                for model in models
            ]
            outbox_event = OutboxEvent(
                subject=self._topics.bulk_update,
                payload=payloads,
            )
            self._session.add(outbox_event)

        return models

    async def delete(self, obj_id: int) -> bool:
        model = await self._returning_delete(obj_id)
        if model:
            payload = self._event_schemas.delete.model_validate(model).model_dump(mode="json")
            outbox_event = OutboxEvent(
                subject=self._topics.delete,
                payload=payload,
            )
            self._session.add(outbox_event)
            return True
        return False

    async def _returning_delete(self, obj_id: int) -> TModel | None:
        stmt = (
            delete(self._model)
            .where(self._model.id == obj_id)
            .returning(self._model)
        )

        try:
            result = await self._session.execute(stmt)
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        return result.scalar_one_or_none()
