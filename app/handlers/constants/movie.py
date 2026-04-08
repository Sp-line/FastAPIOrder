from enum import StrEnum, auto


class MovieDurables(StrEnum):
    ORDER_SVC_MOVIES_CREATED_SYNC_DB = auto()
    ORDER_SVC_MOVIES_BULK_CREATED_SYNC_DB = auto()
    ORDER_SVC_MOVIES_UPDATED_SYNC_DB = auto()
