from sqlalchemy import Column, String, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.user import gen_uuid
from app.models.enums import VehicleType


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(String, primary_key=True, default=gen_uuid)
    plate_number = Column(String, unique=True, nullable=False, index=True)
    type = Column(SAEnum(VehicleType), nullable=False)
    color = Column(String, nullable=True)
    owner_name = Column(String, nullable=True)
    is_blacklisted = Column(Boolean, default=False, nullable=False)

    gate_passes = relationship("GatePass", back_populates="vehicle")

    def __repr__(self):
        return f"<Vehicle {self.plate_number}>"