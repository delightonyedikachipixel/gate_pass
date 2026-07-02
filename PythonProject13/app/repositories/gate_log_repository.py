from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.gate_log import GateLog


class GateLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, gate_log: GateLog) -> GateLog:
        self.db.add(gate_log)
        self.db.commit()
        self.db.refresh(gate_log)
        return gate_log

    def get_by_id(self, gate_log_id: str) -> Optional[GateLog]:
        return self.db.query(GateLog).filter(GateLog.id == gate_log_id).first()

    def list_by_pass(self, gate_pass_id: str) -> List[GateLog]:
        return (
            self.db.query(GateLog)
            .filter(GateLog.gate_pass_id == gate_pass_id)
            .order_by(GateLog.timestamp)
            .all()
        )

    def list_all(self) -> List[GateLog]:
        return self.db.query(GateLog).order_by(GateLog.timestamp.desc()).all()