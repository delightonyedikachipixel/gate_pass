from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.gate import Gate
from app.repositories.gate_repository import GateRepository
from app.schemas.gate import GateCreate


class GateService:
    def __init__(self, db: Session):
        self.repo = GateRepository(db)

    def create_gate(self, payload: GateCreate) -> Gate:
        gate = Gate(**payload.dict())
        return self.repo.create(gate)

    def get_gate(self, gate_id: str) -> Gate:
        gate = self.repo.get_by_id(gate_id)
        if not gate:
            raise HTTPException(status_code=404, detail="Gate not found")
        return gate

    def list_gates(self):
        return self.repo.list_all()