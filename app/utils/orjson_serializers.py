from decimal import Decimal
from enum import StrEnum
from typing import Any, overload

import orjson


@overload
def orjson_default_encoder(obj: Decimal) -> str: ...


@overload
def orjson_default_encoder(obj: StrEnum) -> str: ...


def orjson_default_encoder(obj: Any) -> Any:
    if isinstance(obj, StrEnum):
        return obj.value
    if isinstance(obj, Decimal):
        return str(obj)

    raise TypeError(f"Type {type(obj).__name__} is not JSON serializable")


def orjson_serializer(obj: Any) -> str:
    return orjson.dumps(
        obj,
        default=orjson_default_encoder,
        option=orjson.OPT_NON_STR_KEYS
    ).decode()


def orjson_deserializer(json_str: str | bytes) -> Any:
    return orjson.loads(json_str)
