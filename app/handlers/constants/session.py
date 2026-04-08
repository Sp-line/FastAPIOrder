from enum import StrEnum, auto


class SessionDurables(StrEnum):
    ORDER_SVC_SESSIONS_CREATED_SYNC_DB = auto()
    ORDER_SVC_SESSIONS_BULK_CREATED_SYNC_DB = auto()
    ORDER_SVC_SESSIONS_UPDATED_SYNC_DB = auto()
    ORDER_SVC_SESSIONS_BULK_UPDATED_SYNC_DB = auto()
