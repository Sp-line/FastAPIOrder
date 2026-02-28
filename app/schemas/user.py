from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from constants import UserLimits
from schemas.base import Id


class UserBase(BaseModel):
    email: EmailStr
    first_name: Annotated[str, Field(min_length=UserLimits.FIRST_NAME_MIN, max_length=UserLimits.FIRST_NAME_MAX)]
    last_name: Annotated[str, Field(min_length=UserLimits.LAST_NAME_MIN, max_length=UserLimits.LAST_NAME_MAX)]
    phone_number: Annotated[str | None, Field(min_length=UserLimits.PHONE_MIN, max_length=UserLimits.PHONE_MAX)]


class UserCreateDB(Id, UserBase):
    pass


class UserCreateReq(Id, UserBase):
    pass


class UserUpdateBase(BaseModel):
    email: EmailStr | None = None
    first_name: Annotated[str | None, Field(min_length=UserLimits.FIRST_NAME_MIN, max_length=UserLimits.FIRST_NAME_MAX)] = None
    last_name: Annotated[str | None, Field(min_length=UserLimits.LAST_NAME_MIN, max_length=UserLimits.LAST_NAME_MAX)] = None
    phone_number: Annotated[str | None, Field(min_length=UserLimits.PHONE_MIN, max_length=UserLimits.PHONE_MAX)] = None


class UserUpdateDB(UserUpdateBase):
    pass


class UserUpdateReq(UserUpdateBase):
    pass


class UserRead(Id, UserBase):
    model_config = ConfigDict(from_attributes=True)
