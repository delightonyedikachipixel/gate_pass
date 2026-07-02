from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.user import gen_uuid


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(String, primary_key=True, default=gen_uuid)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    id_type = Column(String, nullable=True)       # e.g. "National ID", "Passport"
    id_number = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    is_blacklisted = Column(Boolean, default=False, nullable=False)

    gate_passes = relationship("GatePass", back_populates="visitor")

    def __repr__(self):
        return f"<Visitor {self.full_name}>"