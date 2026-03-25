from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Any

    from core.models.mixins.int_id_pk import IntIdPkMixin


def build_map[TModel: IntIdPkMixin](data: Iterable[TModel]) -> dict[int, TModel]:
    return {item.id: item for item in data}


def get_ids(data: Iterable[Any], field: str) -> set[int]:
    return {getattr(item, field) for item in data}
