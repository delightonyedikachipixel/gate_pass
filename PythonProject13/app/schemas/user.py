from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import Role


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: Role
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)