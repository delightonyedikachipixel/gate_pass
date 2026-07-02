from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.vehicle import VehicleCreate, VehicleRead
from app.services.vehicle_service import VehicleService

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("/", response_model=VehicleRead, status_code=201)
def register_vehicle(payload: VehicleCreate, db: Session = Depends(get_db)):
    return VehicleService(db).register_vehicle(payload)


@router.get("/", response_model=List[VehicleRead])
def list_vehicles(db: Session = Depends(get_db)):
    return VehicleService(db).list_vehicles()


@router.get("/{vehicle_id}", response_model=VehicleRead)
def get_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    return VehicleService(db).get_vehicle(vehicle_id)


@router.patch("/{vehicle_id}/blacklist", response_model=VehicleRead)
def set_vehicle_blacklist(vehicle_id: str, blacklisted: bool, db: Session = Depends(get_db)):
    return VehicleService(db).set_blacklist(vehicle_id, blacklisted)