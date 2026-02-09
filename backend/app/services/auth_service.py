from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.repositories import user_repo


def register_user(db: Session, username: str, full_name: str, role: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    user = User(username=username, full_name=full_name, role=role, hashed_password=hashed_password)
    return user_repo.create(db, user)


def authenticate_user(db: Session, username: str, password: str) -> str | None:
    user = user_repo.get_by_username(db, username)
    if not user or not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return create_access_token(str(user.id))
