from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username == username))


def create(db: Session, user: User) -> User:
    db.add(user)
    db.flush()
    return user
