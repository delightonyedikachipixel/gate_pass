from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.gate_pass import (
    GatePassCreate,
    GatePassRead,
    GatePassDecision,
    GatePassRevoke,
)
from app.services.gate_pass_service import GatePassService

router = APIRouter(prefix="/gate-passes", tags=["Gate Passes"])


@router.post("/", response_model=GatePassRead, status_code=201)
def request_pass(payload: GatePassCreate, db: Session = Depends(get_db)):
    return GatePassService(db).request_pass(payload)


@router.get("/", response_model=List[GatePassRead])
def list_passes(db: Session = Depends(get_db)):
    return GatePassService(db).list_passes()


@router.get("/pending", response_model=List[GatePassRead])
def list_pending_passes(db: Session = Depends(get_db)):
    return GatePassService(db).list_pending()


@router.get("/verify/{pass_code}", response_model=GatePassRead)
def verify_pass(pass_code: str, db: Session = Depends(get_db)):
    return GatePassService(db).verify_pass(pass_code)


@router.get("/visitor/{visitor_id}", response_model=List[GatePassRead])
def list_passes_for_visitor(visitor_id: str, db: Session = Depends(get_db)):
    return GatePassService(db).list_for_visitor(visitor_id)


@router.get("/vehicle/{vehicle_id}", response_model=List[GatePassRead])
def list_passes_for_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    return GatePassService(db).list_for_vehicle(vehicle_id)



@router.get("/{pass_id}", response_model=GatePassRead)
def get_pass(pass_id: str, db: Session = Depends(get_db)):
    return GatePassService(db).get_pass(pass_id)


@router.post("/{pass_id}/approve", response_model=GatePassRead)
def approve_pass(pass_id: str, payload: GatePassDecision, db: Session = Depends(get_db)):
    return GatePassService(db).approve_pass(pass_id, payload)


@router.post("/{pass_id}/reject", response_model=GatePassRead)
def reject_pass(pass_id: str, payload: GatePassDecision, db: Session = Depends(get_db)):
    return GatePassService(db).reject_pass(pass_id, payload)


@router.post("/{pass_id}/revoke", response_model=GatePassRead)
def revoke_pass(pass_id: str, payload: GatePassRevoke, db: Session = Depends(get_db)):
    return GatePassService(db).revoke_pass(pass_id, payload)