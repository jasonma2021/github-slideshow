from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut
from app.services.order_service import create_order
from app.repositories import order_repo

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut)
def create_sales_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        with db.begin():
            order = create_order(
                db,
                payload.customer_id,
                [item.model_dump() for item in payload.items],
                user.id,
            )
        return order
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return order_repo.list_all(db)
