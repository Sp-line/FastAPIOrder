from enum import StrEnum


class OrderLimits:
    PUBLIC_CODE_MAX: int = 6
    PUBLIC_CODE_ALPHABET: str = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"

    STATUS_MAX: int = 25

    EXPIRE_SCHEDULE_ID_MAX: int = 255
    EXPIRE_SCHEDULE_ID_UNIQUE: bool = True

    EXPIRE_MINUTES: int = 10

    PUBLIC_ID_UNIQUE: bool = True

    ORDER_NUMBER_UNIQUE: bool = True


class OrderStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    EXPIRED = "expired"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUND_PENDING = "refund_pending"
    REFUNDED = "refunded"
