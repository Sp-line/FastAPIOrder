from enum import StrEnum


class SessionLimits:
    DIMENSION_FORMAT_MAX: int = 25
    SCREEN_TECHNOLOGY_MAX: int = 25


class DimensionFormat(StrEnum):
    TWO_D = "2d"
    THREE_D = "3d"


class ScreenTechnology(StrEnum):
    STANDARD = "standard"
    IMAX = "imax"
    IMAX_LASER = "imax_laser"
    DX_4 = "4dx"
    DOLBY_CINEMA = "dolby_cinema"
    SCREENX = "screenx"
    ONYX = "onyx"
    