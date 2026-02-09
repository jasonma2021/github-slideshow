from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.constants import UserRole
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import register_user

router = APIRouter(prefix="/users", tags=["users"])


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user


@router.post("", response_model=UserOut)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    user = register_user(db, payload.username, payload.full_name, payload.role, payload.password)
    return user
