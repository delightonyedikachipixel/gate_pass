from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.gate_log import GateLog
from app.models.enums import Direction, PassStatus
from app.repositories.gate_log_repository import GateLogRepository
from app.repositories.gate_pass_repository import GatePassRepository
from app.repositories.gate_repository import GateRepository
from app.repositories.user_repository import UserRepository
from app.schemas.gate_log import GateLogCreate


class GateLogService:
    def __init__(self, db: Session):
        self.repo = GateLogRepository(db)
        self.pass_repo = GatePassRepository(db)
        self.gate_repo = GateRepository(db)
        self.user_repo = UserRepository(db)

    def record_entry(self, payload: GateLogCreate) -> GateLog:
        return self._record(payload, expected_direction=Direction.ENTRY)

    def record_exit(self, payload: GateLogCreate) -> GateLog:
        return self._record(payload, expected_direction=Direction.EXIT)

    def _record(self, payload: GateLogCreate, expected_direction: Direction) -> GateLog:
        if payload.direction != expected_direction:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Direction mismatch: expected {expected_direction}",
            )

        gate_pass = self.pass_repo.get_by_id(payload.gate_pass_id)
        if not gate_pass:
            raise HTTPException(status_code=404, detail="Gate pass not found")

        gate = self.gate_repo.get_by_id(payload.gate_id)
        if not gate:
            raise HTTPException(status_code=404, detail="Gate not found")
        if not gate.is_active:
            raise HTTPException(status_code=400, detail="Gate is not active")

        scanner = self.user_repo.get_by_id(payload.scanned_by_id)
        if not scanner:
            raise HTTPException(status_code=404, detail="Scanning user not found")

        if not gate_pass.is_valid_now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Gate pass is not currently valid (status={gate_pass.status})",
            )

        log = GateLog(
            gate_pass_id=gate_pass.id,
            gate_id=gate.id,
            scanned_by_id=scanner.id,
            direction=expected_direction,
            notes=payload.notes,
        )
        log = self.repo.create(log)

       
        if expected_direction == Direction.ENTRY and gate_pass.status == PassStatus.APPROVED:
            gate_pass.status = PassStatus.ACTIVE
            self.pass_repo.save(gate_pass)
        elif expected_direction == Direction.EXIT and not gate_pass.is_multi_entry:
            gate_pass.status = PassStatus.COMPLETED
            self.pass_repo.save(gate_pass)

        return log

    def list_for_pass(self, gate_pass_id: str):
        return self.repo.list_by_pass(gate_pass_id)

    def list_all(self):
        return self.repo.list_all()