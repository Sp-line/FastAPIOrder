from __future__ import annotations

from typing import (
    Iterable,
    Any,
    TYPE_CHECKING
)

from core.models import (
    SessionPrice,
    Seat
)
from exceptions.db import ObjectNotFoundException
from repositories import (
    SessionPriceRepository,
    UnitOfWork
)
from schemas.session_price import (
    SessionPriceRead,
    SessionPriceCreateReq,
    SessionPriceUpdateReq,
    SessionPriceCreateDB,
    SessionPriceUpdateDB,
)
from services import (
    ServiceBase,
    DataExistenceServiceBase
)


if TYPE_CHECKING:
    from constants import SeatType
    from decimal import Decimal
    from app_types import (
        PriceMap,
        IntMap
    )


class SessionPriceService(
    ServiceBase[
        SessionPriceRepository,
        SessionPriceRead,
        SessionPriceCreateReq,
        SessionPriceUpdateReq,
        SessionPriceCreateDB,
        SessionPriceUpdateDB,
    ],
):
    def __init__(self, repository: SessionPriceRepository, unit_of_work: UnitOfWork) -> None:
        super().__init__(
            repository=repository,
            unit_of_work=unit_of_work,
            table_name="session_prices",
            read_schema=SessionPriceRead,
            db_create_schema=SessionPriceCreateDB,
            db_update_schema=SessionPriceUpdateDB,
        )


class SessionPriceDataExistenceService(
    DataExistenceServiceBase[
        SessionPrice,
    ]
):
    def __init__(self) -> None:
        super().__init__(
            table_name="session_prices"
        )

    def ensure_prices_exist(
            self,
            data: Iterable[Any],
            seats_map: IntMap[Seat],
            prices_map: PriceMap
    ) -> None:
        for item in data:
            seat_id = self._get_obj_id_from_item(item, "seat_id")
            session_id = self._get_obj_id_from_item(item, "session_id")

            seat_type = seats_map[seat_id].type
            if (session_id, seat_type) not in prices_map:
                raise ObjectNotFoundException(
                    conditions={
                        "session_id": session_id,
                        "seat_type": seat_type
                    },
                    table_name=self._table_name,
                )

    def ensure_price_exist(
            self,
            session_id: int,
            seat_type: SeatType,
            price: Decimal | None
    ) -> Decimal:
        if not price:
            raise ObjectNotFoundException(
                conditions={
                    "session_id": session_id,
                    "seat_type": seat_type
                },
                table_name=self._table_name,
            )
        return price
