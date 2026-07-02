from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.gate_log import GateLogCreate, GateLogRead
from app.services.gate_log_service import GateLogService

router = APIRouter(prefix="/gate-logs", tags=["Gate Logs"])


@router.post("/entry", response_model=GateLogRead, status_code=201)
def record_entry(payload: GateLogCreate, db: Session = Depends(get_db)):
    return GateLogService(db).record_entry(payload)


@router.post("/exit", response_model=GateLogRead, status_code=201)
def record_exit(payload: GateLogCreate, db: Session = Depends(get_db)):
    return GateLogService(db).record_exit(payload)


@router.get("/", response_model=List[GateLogRead])
def list_logs(db: Session = Depends(get_db)):
    return GateLogService(db).list_all()


@router.get("/pass/{gate_pass_id}", response_model=List[GateLogRead])
def list_logs_for_pass(gate_pass_id: str, db: Session = Depends(get_db)):
    return GateLogService(db).list_for_pass(gate_pass_id)