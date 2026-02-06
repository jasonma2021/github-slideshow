from pydantic import BaseModel

from app.core.constants import UserRole


class UserCreate(BaseModel):
    username: str
    full_name: str
    role: UserRole
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    role: UserRole
    is_active: bool

    class Config:
        from_attributes = True
