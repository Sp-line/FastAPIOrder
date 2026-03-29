from core import fs_router
from schemas.base import Id
from schemas.events import CRUDEventPublishers
from schemas.ticket import (
    TicketCreateEvent,
    TicketUpdateEvent
)

ticket_created = fs_router.publisher(
    "purchases.tickets.created",
    schema=TicketCreateEvent,
)

ticket_bulk_created = fs_router.publisher(
    "purchases.tickets.bulk.created",
    schema=list[TicketCreateEvent],
)

ticket_updated = fs_router.publisher(
    "purchases.tickets.updated",
    schema=TicketUpdateEvent,
)

ticket_bulk_updated = fs_router.publisher(
    "purchases.tickets.bulk.updated",
    schema=list[TicketUpdateEvent],
)

ticket_deleted = fs_router.publisher(
    "purchases.tickets.deleted",
    schema=Id,
)

ticket_crud_publishers = CRUDEventPublishers(
    create_pub=ticket_created,
    bulk_create_pub=ticket_bulk_created,
    update_pub=ticket_updated,
    bulk_update_pub=ticket_bulk_updated,
    delete_pub=ticket_deleted,
)
