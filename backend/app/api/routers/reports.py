from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.order import SalesOrder
from app.models.stock import StockBalance
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/sales")
def sales_report(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    total_sales = db.scalar(func.coalesce(func.sum(SalesOrder.total_amount), 0))
    return {"total_sales": float(total_sales)}


@router.get("/inventory")
def inventory_report(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.query(StockBalance.product_id, StockBalance.quantity).all()
    return {"items": [{"product_id": row[0], "quantity": row[1]} for row in rows]}
