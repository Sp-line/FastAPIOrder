from decimal import Decimal
from enum import StrEnum


class TicketLimits:
    PRICE_MIN: Decimal = Decimal("0.00")

    CODE_UNIQUE: bool = True

    STATUS_MAX: int = 20


class TicketStatus(StrEnum):
    RESERVED = "reserved"
    PAID = "paid"
    USED = "used"
    EXPIRED = "expired"
    REFUND_PENDING = "refund_pending"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"
