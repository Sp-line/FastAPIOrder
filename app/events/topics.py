from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True)
class CRUDTopics:
    create: str
    bulk_create: str
    update: str
    bulk_update: str
    delete: str

    @classmethod
    def generate(cls, microservice: str, table_name: str) -> Self:
        prefix = f"{microservice}.{table_name}"
        return cls(
            create=f"{prefix}.created",
            bulk_create=f"{prefix}.bulk.created",
            update=f"{prefix}.updated",
            bulk_update=f"{prefix}.bulk.updated",
            delete=f"{prefix}.deleted"
        )
