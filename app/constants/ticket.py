from decimal import Decimal
from enum import StrEnum


class TicketLimits:
    PRICE_MIN: Decimal = Decimal("0.00")

    CODE_UNIQUE: bool = True

    STATUS_MAX: int = 20


class TicketStatus(StrEnum):
    RESERVED = "reserved"
    ACTIVE = "active"
    USED = "used"
    EXPIRED = "expired"
    RETURNED = "returned"
    CANCELLED = "cancelled"
