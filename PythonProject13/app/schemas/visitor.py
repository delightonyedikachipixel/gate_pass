from typing import Optional

from pydantic import BaseModel, ConfigDict


class VisitorBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    id_type: Optional[str] = None
    id_number: Optional[str] = None
    company_name: Optional[str] = None


class VisitorCreate(VisitorBase):
    pass


class VisitorRead(VisitorBase):
    id: str
    is_blacklisted: bool

    model_config = ConfigDict(from_attributes=True)