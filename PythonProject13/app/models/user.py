import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.enums import Role


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=gen_uuid)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(SAEnum(Role), nullable=False)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    requested_passes = relationship(
        "GatePass",
        back_populates="requested_by",
        foreign_keys="GatePass.requested_by_id",
    )
    approved_passes = relationship(
        "GatePass",
        back_populates="approved_by",
        foreign_keys="GatePass.approved_by_id",
    )
    gate_logs = relationship("GateLog", back_populates="scanned_by")

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"