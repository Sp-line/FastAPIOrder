from dataclasses import dataclass

from services import UserDataExistenceService


@dataclass(frozen=True, slots=True)
class BulkCreateOrderDataExistenceServices:
    user: UserDataExistenceService
