from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.visitor import VisitorCreate, VisitorRead
from app.services.visitor_service import VisitorService

router = APIRouter(prefix="/visitors", tags=["Visitors"])


@router.post("/", response_model=VisitorRead, status_code=201)
def register_visitor(payload: VisitorCreate, db: Session = Depends(get_db)):
    return VisitorService(db).register_visitor(payload)


@router.get("/", response_model=List[VisitorRead])
def list_visitors(db: Session = Depends(get_db)):
    return VisitorService(db).list_visitors()


@router.get("/{visitor_id}", response_model=VisitorRead)
def get_visitor(visitor_id: str, db: Session = Depends(get_db)):
    return VisitorService(db).get_visitor(visitor_id)


@router.patch("/{visitor_id}/blacklist", response_model=VisitorRead)
def set_visitor_blacklist(visitor_id: str, blacklisted: bool, db: Session = Depends(get_db)):
    return VisitorService(db).set_blacklist(visitor_id, blacklisted)