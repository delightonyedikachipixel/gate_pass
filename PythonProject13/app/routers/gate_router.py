from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.gate import GateCreate, GateRead
from app.services.gate_service import GateService

router = APIRouter(prefix="/gates", tags=["Gates"])


@router.post("/", response_model=GateRead, status_code=201)
def create_gate(payload: GateCreate, db: Session = Depends(get_db)):
    return GateService(db).create_gate(payload)


@router.get("/", response_model=List[GateRead])
def list_gates(db: Session = Depends(get_db)):
    return GateService(db).list_gates()


@router.get("/{gate_id}", response_model=GateRead)
def get_gate(gate_id: str, db: Session = Depends(get_db)):
    return GateService(db).get_gate(gate_id)