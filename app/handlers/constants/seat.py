from enum import StrEnum, auto


class SeatDurables(StrEnum):
    SESSION_SVC_SEATS_CREATED_SYNC_DB = auto()
    SESSION_SVC_SEATS_BULK_CREATED_SYNC_DB = auto()
    SESSION_SVC_SEATS_UPDATED_SYNC_DB = auto()
    SESSION_SVC_SEATS_BULK_UPDATED_SYNC_DB = auto()
