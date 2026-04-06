from enum import StrEnum, auto


class MovieDurables(StrEnum):
    MOVIE_SVC_MOVIES_CREATED_SYNC_DB = auto()
    MOVIE_SVC_MOVIES_BULK_CREATED_SYNC_DB = auto()
    MOVIE_SVC_MOVIES_UPDATED_SYNC_DB = auto()
