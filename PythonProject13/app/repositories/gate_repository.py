from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.gate import Gate


class GateRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, gate: Gate) -> Gate:
        self.db.add(gate)
        self.db.commit()
        self.db.refresh(gate)
        return gate

    def get_by_id(self, gate_id: str) -> Optional[Gate]:
        return self.db.query(Gate).filter(Gate.id == gate_id).first()

    def list_all(self) -> List[Gate]:
        return self.db.query(Gate).all()