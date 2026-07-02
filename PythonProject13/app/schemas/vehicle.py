from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import VehicleType


class VehicleBase(BaseModel):
    plate_number: str
    type: VehicleType
    color: Optional[str] = None
    owner_name: Optional[str] = None


class VehicleCreate(VehicleBase):
    pass


class VehicleRead(VehicleBase):
    id: str
    is_blacklisted: bool

    model_config = ConfigDict(from_attributes=True)