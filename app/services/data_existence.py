from __future__ import annotations

from typing import TYPE_CHECKING

from core.models.mixins.int_id_pk import IntIdPkMixin
from exceptions.db import ObjectNotFoundException

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Any


class DataExistenceServiceBase[TModel: IntIdPkMixin]:
    def __init__(self, table_name: str) -> None:
        self._table_name = table_name

    @staticmethod
    def _get_obj_id_from_item(item: Any, field: str) -> int:
        obj_id = getattr(item, field, None)

        if obj_id is None:
            raise ValueError(
                f"Error: Object {item.__class__.__name__} "
                f"does not have attribute '{field}'."
            )

        if not isinstance(obj_id, int):
            raise ValueError(
                f"Error: field {field} is not an integer."
            )

        return obj_id

    def ensure_obj_exist(self, obj_id: int, obj: TModel | None) -> TModel:
        if not obj:
            raise ObjectNotFoundException(obj_id=obj_id, table_name=self._table_name)
        return obj

    def ensure_objs_exist(
            self,
            data: Iterable[Any],
            obj_id_field: str,
            objs_map: dict[int, TModel],
    ) -> None:
        for item in data:
            obj_id = self._get_obj_id_from_item(item, obj_id_field)

            if obj_id not in objs_map:
                raise ObjectNotFoundException(obj_id=obj_id, table_name=self._table_name)
