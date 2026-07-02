from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.enums import PassType, PassStatus
from app.schemas.visitor import VisitorRead
from app.schemas.vehicle import VehicleRead
from app.schemas.user import UserRead


class GatePassCreate(BaseModel):
    purpose: Optional[str] = None
    type: PassType
    valid_from: datetime
    valid_to: datetime
    is_multi_entry: bool = False

    requested_by_id: str
    visitor_id: Optional[str] = None
    vehicle_id: Optional[str] = None

    @model_validator(mode="after")
    def check_required_links(self):
        if self.type == PassType.VISITOR and not self.visitor_id:
            raise ValueError("visitor_id is required for a VISITOR pass")
        if self.type == PassType.VEHICLE and not self.vehicle_id:
            raise ValueError("vehicle_id is required for a VEHICLE pass")
        if self.type == PassType.VISITOR_WITH_VEHICLE and not (self.visitor_id and self.vehicle_id):
            raise ValueError(
                "both visitor_id and vehicle_id are required for a VISITOR_WITH_VEHICLE pass"
            )

        if self.valid_from and self.valid_to and self.valid_to <= self.valid_from:
            raise ValueError("valid_to must be after valid_from")

        return self


class GatePassRead(BaseModel):
    id: str
    pass_code: str
    purpose: Optional[str]
    type: PassType
    status: PassStatus
    valid_from: datetime
    valid_to: datetime
    is_multi_entry: bool
    qr_code_url: Optional[str]
    created_at: datetime

    requested_by: UserRead
    approved_by: Optional[UserRead]
    visitor: Optional[VisitorRead]
    vehicle: Optional[VehicleRead]

    model_config = ConfigDict(from_attributes=True)


class GatePassDecision(BaseModel):
    approver_id: str
    reason: Optional[str] = None


class GatePassRevoke(BaseModel):
    reason: Optional[str] = None