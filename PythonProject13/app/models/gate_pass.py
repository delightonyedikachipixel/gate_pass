import secrets
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.user import gen_uuid
from app.models.enums import PassType, PassStatus


def gen_pass_code():
    return secrets.token_hex(4).upper()  # e.g. "A1B2C3D4"


class GatePass(Base):
    __tablename__ = "gate_passes"

    id = Column(String, primary_key=True, default=gen_uuid)
    pass_code = Column(String, unique=True, nullable=False, default=gen_pass_code)
    purpose = Column(String, nullable=True)
    type = Column(SAEnum(PassType), nullable=False)
    status = Column(SAEnum(PassStatus), nullable=False, default=PassStatus.PENDING)
    valid_from = Column(DateTime, nullable=False)
    valid_to = Column(DateTime, nullable=False)
    is_multi_entry = Column(Boolean, default=False, nullable=False)
    qr_code_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    requested_by_id = Column(String, ForeignKey("users.id"), nullable=False)
    approved_by_id = Column(String, ForeignKey("users.id"), nullable=True)
    visitor_id = Column(String, ForeignKey("visitors.id"), nullable=True)
    vehicle_id = Column(String, ForeignKey("vehicles.id"), nullable=True)

    requested_by = relationship(
        "User", back_populates="requested_passes", foreign_keys=[requested_by_id]
    )
    approved_by = relationship(
        "User", back_populates="approved_passes", foreign_keys=[approved_by_id]
    )
    visitor = relationship("Visitor", back_populates="gate_passes")
    vehicle = relationship("Vehicle", back_populates="gate_passes")
    gate_logs = relationship("GateLog", back_populates="gate_pass")


    def approve(self, approver_id: str):
        self.status = PassStatus.APPROVED
        self.approved_by_id = approver_id

    def reject(self, reason: str = None):
        self.status = PassStatus.REJECTED
        if reason:
            self.purpose = f"{self.purpose or ''} [REJECTED: {reason}]".strip()

    def revoke(self, reason: str = None):
        self.status = PassStatus.REVOKED
        if reason:
            self.purpose = f"{self.purpose or ''} [REVOKED: {reason}]".strip()

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.valid_to

    def is_valid_now(self) -> bool:
        now = datetime.utcnow()
        return (
            self.status in (PassStatus.APPROVED, PassStatus.ACTIVE)
            and self.valid_from <= now <= self.valid_to
        )

    def __repr__(self):
        return f"<GatePass {self.pass_code} ({self.status})>"