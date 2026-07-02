from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.vehicle import Vehicle


class VehicleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, vehicle: Vehicle) -> Vehicle:
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def get_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def get_by_plate(self, plate_number: str) -> Optional[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.plate_number == plate_number).first()

    def list_all(self) -> List[Vehicle]:
        return self.db.query(Vehicle).all()

    def set_blacklisted(self, vehicle_id: str, blacklisted: bool) -> Optional[Vehicle]:
        vehicle = self.get_by_id(vehicle_id)
        if vehicle:
            vehicle.is_blacklisted = blacklisted
            self.db.commit()
            self.db.refresh(vehicle)
        return vehicle