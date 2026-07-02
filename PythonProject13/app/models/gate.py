from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.user import gen_uuid


class Gate(Base):
    __tablename__ = "gates"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    gate_logs = relationship("GateLog", back_populates="gate")

    def __repr__(self):
        return f"<Gate {self.name}>"