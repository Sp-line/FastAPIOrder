from enum import StrEnum, auto


class HallDurables(StrEnum):
    SESSION_SVC_HALLS_CREATED_SYNC_DB = auto()
    SESSION_SVC_HALLS_BULK_CREATED_SYNC_DB = auto()
    SESSION_SVC_HALLS_UPDATED_SYNC_DB = auto()
    SESSION_SVC_HALLS_BULK_UPDATED_SYNC_DB = auto()
