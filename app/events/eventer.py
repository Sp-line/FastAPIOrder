from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from faststream.nats.publisher.usecase import LogicPublisher
    from typing import Any
    from app_types import AsyncEventFactory
    from schemas.events import CRUDEventPublishers


class Eventer[
    TCreateEventSchema: BaseModel,
    TUpdateEventSchema: BaseModel,
    TDeleteEventSchema: BaseModel,
]:
    def __init__(self, publishers: CRUDEventPublishers) -> None:
        self.publishers = publishers

    @staticmethod
    def _event_factory(publisher: LogicPublisher, payload: Any) -> AsyncEventFactory:
        async def factory():
            await publisher.publish(payload)

        return factory

    def create(self, payload: TCreateEventSchema) -> AsyncEventFactory:
        return self._event_factory(self.publishers.create_pub, payload)

    def bulk_create(self, payload: list[TCreateEventSchema]) -> AsyncEventFactory:
        return self._event_factory(self.publishers.bulk_create_pub, payload)

    def update(self, payload: TUpdateEventSchema) -> AsyncEventFactory:
        return self._event_factory(self.publishers.update_pub, payload)

    def bulk_update(self, payload: list[TUpdateEventSchema]) -> AsyncEventFactory:
        return self._event_factory(self.publishers.bulk_update_pub, payload)

    def delete(self, payload: TDeleteEventSchema) -> AsyncEventFactory:
        return self._event_factory(self.publishers.delete_pub, payload)
