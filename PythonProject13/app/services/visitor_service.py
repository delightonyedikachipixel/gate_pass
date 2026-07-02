from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.visitor import Visitor
from app.repositories.visitor_repository import VisitorRepository
from app.schemas.visitor import VisitorCreate


class VisitorService:
    def __init__(self, db: Session):
        self.repo = VisitorRepository(db)

    def register_visitor(self, payload: VisitorCreate) -> Visitor:
        visitor = Visitor(**payload.dict())
        return self.repo.create(visitor)

    def get_visitor(self, visitor_id: str) -> Visitor:
        visitor = self.repo.get_by_id(visitor_id)
        if not visitor:
            raise HTTPException(status_code=404, detail="Visitor not found")
        return visitor

    def list_visitors(self):
        return self.repo.list_all()

    def set_blacklist(self, visitor_id: str, blacklisted: bool) -> Visitor:
        visitor = self.repo.set_blacklisted(visitor_id, blacklisted)
        if not visitor:
            raise HTTPException(status_code=404, detail="Visitor not found")
        return visitor