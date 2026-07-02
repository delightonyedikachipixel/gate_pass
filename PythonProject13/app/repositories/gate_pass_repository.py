from typing import Optional, List

from sqlalchemy.orm import Session, joinedload

from app.models.gate_pass import GatePass


class GatePassRepository:
    def __init__(self, db: Session):
        self.db = db

    def _base_query(self):
        return self.db.query(GatePass).options(
            joinedload(GatePass.requested_by),
            joinedload(GatePass.approved_by),
            joinedload(GatePass.visitor),
            joinedload(GatePass.vehicle),
        )

    def create(self, gate_pass: GatePass) -> GatePass:
        self.db.add(gate_pass)
        self.db.commit()
        self.db.refresh(gate_pass)
        return gate_pass

    def get_by_id(self, pass_id: str) -> Optional[GatePass]:
        return self._base_query().filter(GatePass.id == pass_id).first()

    def get_by_code(self, pass_code: str) -> Optional[GatePass]:
        return self._base_query().filter(GatePass.pass_code == pass_code).first()

    def list_all(self) -> List[GatePass]:
        return self._base_query().all()

    def list_by_visitor(self, visitor_id: str) -> List[GatePass]:
        return self._base_query().filter(GatePass.visitor_id == visitor_id).all()

    def list_by_vehicle(self, vehicle_id: str) -> List[GatePass]:
        return self._base_query().filter(GatePass.vehicle_id == vehicle_id).all()

    def list_pending(self) -> List[GatePass]:
        from app.models.enums import PassStatus
        return self._base_query().filter(GatePass.status == PassStatus.PENDING).all()

    def save(self, gate_pass: GatePass) -> GatePass:
        self.db.commit()
        self.db.refresh(gate_pass)
        return gate_pass