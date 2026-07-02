import hashlib

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


def _hash_password(raw: str) -> str:
    
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, payload: UserCreate) -> User:
        existing = self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A user with email {payload.email} already exists",
            )
        user = User(
            full_name=payload.full_name,
            email=payload.email,
            password_hash=_hash_password(payload.password),
            role=payload.role,
            phone=payload.phone,
        )
        return self.repo.create(user)

    def get_user(self, user_id: str) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def list_users(self):
        return self.repo.list_all()