from typing import Optional

from pydantic import BaseModel, ConfigDict


class GateBase(BaseModel):
    name: str
    location: Optional[str] = None


class GateCreate(GateBase):
    pass


class GateRead(GateBase):
    id: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)