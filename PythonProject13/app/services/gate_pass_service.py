from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.gate_pass import GatePass
from app.models.enums import PassStatus
from app.repositories.gate_pass_repository import GatePassRepository
from app.repositories.user_repository import UserRepository
from app.repositories.visitor_repository import VisitorRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.gate_pass import GatePassCreate, GatePassDecision, GatePassRevoke


class GatePassService:
    def __init__(self, db: Session):
        self.repo = GatePassRepository(db)
        self.user_repo = UserRepository(db)
        self.visitor_repo = VisitorRepository(db)
        self.vehicle_repo = VehicleRepository(db)

    def request_pass(self, payload: GatePassCreate) -> GatePass:
        requester = self.user_repo.get_by_id(payload.requested_by_id)
        if not requester:
            raise HTTPException(status_code=404, detail="Requesting user not found")

        if payload.visitor_id:
            visitor = self.visitor_repo.get_by_id(payload.visitor_id)
            if not visitor:
                raise HTTPException(status_code=404, detail="Visitor not found")
            if visitor.is_blacklisted:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Visitor {visitor.full_name} is blacklisted and cannot be issued a pass",
                )

        if payload.vehicle_id:
            vehicle = self.vehicle_repo.get_by_id(payload.vehicle_id)
            if not vehicle:
                raise HTTPException(status_code=404, detail="Vehicle not found")
            if vehicle.is_blacklisted:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Vehicle {vehicle.plate_number} is blacklisted and cannot be issued a pass",
                )

        gate_pass = GatePass(
            purpose=payload.purpose,
            type=payload.type,
            status=PassStatus.PENDING,
            valid_from=payload.valid_from,
            valid_to=payload.valid_to,
            is_multi_entry=payload.is_multi_entry,
            requested_by_id=payload.requested_by_id,
            visitor_id=payload.visitor_id,
            vehicle_id=payload.vehicle_id,
        )
        gate_pass = self.repo.create(gate_pass)
        gate_pass.qr_code_url = self._generate_qr_code(gate_pass)
        return self.repo.save(gate_pass)

    def _generate_qr_code(self, gate_pass: GatePass) -> str:

        return f"/qr/{gate_pass.pass_code}"

    def approve_pass(self, pass_id: str, payload: GatePassDecision) -> GatePass:
        gate_pass = self._get_or_404(pass_id)
        if gate_pass.status != PassStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot approve a pass in status {gate_pass.status}",
            )
        approver = self.user_repo.get_by_id(payload.approver_id)
        if not approver:
            raise HTTPException(status_code=404, detail="Approver not found")

        gate_pass.approve(approver.id)
        gate_pass = self.repo.save(gate_pass)
        self._notify(gate_pass, event="APPROVED")
        return gate_pass

    def reject_pass(self, pass_id: str, payload: GatePassDecision) -> GatePass:
        gate_pass = self._get_or_404(pass_id)
        if gate_pass.status != PassStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot reject a pass in status {gate_pass.status}",
            )
        gate_pass.reject(payload.reason)
        gate_pass = self.repo.save(gate_pass)
        self._notify(gate_pass, event="REJECTED")
        return gate_pass

    def revoke_pass(self, pass_id: str, payload: GatePassRevoke) -> GatePass:
        gate_pass = self._get_or_404(pass_id)
        if gate_pass.status in (PassStatus.REVOKED, PassStatus.REJECTED, PassStatus.EXPIRED):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot revoke a pass already in status {gate_pass.status}",
            )
        gate_pass.revoke(payload.reason)
        gate_pass = self.repo.save(gate_pass)
        self._notify(gate_pass, event="REVOKED")
        return gate_pass

    def verify_pass(self, pass_code: str) -> GatePass:

        gate_pass = self.repo.get_by_code(pass_code)
        if not gate_pass:
            raise HTTPException(status_code=404, detail="No gate pass found with that code")

        if gate_pass.visitor and gate_pass.visitor.is_blacklisted:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Associated visitor is blacklisted",
            )
        if gate_pass.vehicle and gate_pass.vehicle.is_blacklisted:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Associated vehicle is blacklisted",
            )

        if gate_pass.is_expired() and gate_pass.status not in (
            PassStatus.EXPIRED, PassStatus.COMPLETED, PassStatus.REVOKED,
        ):
            gate_pass.status = PassStatus.EXPIRED
            gate_pass = self.repo.save(gate_pass)

        if not gate_pass.is_valid_now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Gate pass is not currently valid (status={gate_pass.status})",
            )

        return gate_pass

    def get_pass(self, pass_id: str) -> GatePass:
        return self._get_or_404(pass_id)

    def list_passes(self):
        return self.repo.list_all()

    def list_pending(self):
        return self.repo.list_pending()

    def list_for_visitor(self, visitor_id: str):
        return self.repo.list_by_visitor(visitor_id)

    def list_for_vehicle(self, vehicle_id: str):
        return self.repo.list_by_vehicle(vehicle_id)

    def _get_or_404(self, pass_id: str) -> GatePass:
        gate_pass = self.repo.get_by_id(pass_id)
        if not gate_pass:
            raise HTTPException(status_code=404, detail="Gate pass not found")
        return gate_pass

    def _notify(self, gate_pass: GatePass, event: str):

        pass