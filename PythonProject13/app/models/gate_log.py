from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.user import gen_uuid
from app.models.enums import Direction


class GateLog(Base):
    __tablename__ = "gate_logs"

    id = Column(String, primary_key=True, default=gen_uuid)
    direction = Column(SAEnum(Direction), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(String, nullable=True)

    gate_pass_id = Column(String, ForeignKey("gate_passes.id"), nullable=False)
    gate_id = Column(String, ForeignKey("gates.id"), nullable=False)
    scanned_by_id = Column(String, ForeignKey("users.id"), nullable=False)

    gate_pass = relationship("GatePass", back_populates="gate_logs")
    gate = relationship("Gate", back_populates="gate_logs")
    scanned_by = relationship("User", back_populates="gate_logs")

    def __repr__(self):
        return f"<GateLog {self.direction} @ {self.timestamp}>"