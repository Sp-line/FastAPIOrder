from pydantic import BaseModel, PositiveInt, ConfigDict


class Id(BaseModel):
    id: PositiveInt

    model_config = ConfigDict(from_attributes=True)