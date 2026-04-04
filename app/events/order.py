from core import fs_router
from schemas.base import Id
from schemas.order import (
    OrderCreateEvent,
    OrderUpdateEvent
)

order_created = fs_router.publisher(
    "purchases.orders.created",
    schema=OrderCreateEvent,
)

order_bulk_created = fs_router.publisher(
    "purchases.orders.bulk.created",
    schema=list[OrderCreateEvent],
)

order_updated = fs_router.publisher(
    "purchases.orders.updated",
    schema=OrderUpdateEvent,
)

order_bulk_updated = fs_router.publisher(
    "purchases.orders.bulk.updated",
    schema=list[OrderUpdateEvent],
)

order_deleted = fs_router.publisher(
    "purchases.orders.deleted",
    schema=Id,
)
