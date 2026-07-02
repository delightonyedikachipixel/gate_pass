from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.vehicle import Vehicle
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.vehicle import VehicleCreate


class VehicleService:
    def __init__(self, db: Session):
        self.repo = VehicleRepository(db)

    def register_vehicle(self, payload: VehicleCreate) -> Vehicle:
        existing = self.repo.get_by_plate(payload.plate_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vehicle with plate {payload.plate_number} already registered",
            )
        vehicle = Vehicle(**payload.dict())
        return self.repo.create(vehicle)

    def get_vehicle(self, vehicle_id: str) -> Vehicle:
        vehicle = self.repo.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return vehicle

    def list_vehicles(self):
        return self.repo.list_all()

    def set_blacklist(self, vehicle_id: str, blacklisted: bool) -> Vehicle:
        vehicle = self.repo.set_blacklisted(vehicle_id, blacklisted)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return vehicle