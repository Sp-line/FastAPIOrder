from enum import StrEnum, auto


class HallDurables(StrEnum):
    ORDER_SVC_HALLS_CREATED_SYNC_DB = auto()
    ORDER_SVC_HALLS_BULK_CREATED_SYNC_DB = auto()
    ORDER_SVC_HALLS_UPDATED_SYNC_DB = auto()
    ORDER_SVC_HALLS_BULK_UPDATED_SYNC_DB = auto()
