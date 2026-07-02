from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import Direction


class GateLogCreate(BaseModel):
    gate_pass_id: str
    gate_id: str
    scanned_by_id: str
    direction: Direction
    notes: Optional[str] = None


class GateLogRead(BaseModel):
    id: str
    direction: Direction
    timestamp: datetime
    notes: Optional[str]
    gate_pass_id: str
    gate_id: str
    scanned_by_id: str

    model_config = ConfigDict(from_attributes=True)