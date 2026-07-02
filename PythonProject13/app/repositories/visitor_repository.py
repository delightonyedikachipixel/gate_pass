from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.visitor import Visitor


class VisitorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, visitor: Visitor) -> Visitor:
        self.db.add(visitor)
        self.db.commit()
        self.db.refresh(visitor)
        return visitor

    def get_by_id(self, visitor_id: str) -> Optional[Visitor]:
        return self.db.query(Visitor).filter(Visitor.id == visitor_id).first()

    def list_all(self) -> List[Visitor]:
        return self.db.query(Visitor).all()

    def set_blacklisted(self, visitor_id: str, blacklisted: bool) -> Optional[Visitor]:
        visitor = self.get_by_id(visitor_id)
        if visitor:
            visitor.is_blacklisted = blacklisted
            self.db.commit()
            self.db.refresh(visitor)
        return visitor