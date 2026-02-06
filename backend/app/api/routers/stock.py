from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.stock import StockDocumentOut, StockInCreate, StockOutCreate
from app.services.stock_service import stock_in, stock_out_for_order

router = APIRouter(prefix="/stock", tags=["stock"])


@router.post("/in", response_model=StockDocumentOut)
def create_stock_in(
    payload: StockInCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    with db.begin():
        return stock_in(db, payload.doc_no, [item.model_dump() for item in payload.items], user.id)


@router.post("/out", response_model=StockDocumentOut)
def create_stock_out(
    payload: StockOutCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        with db.begin():
            return stock_out_for_order(db, payload.order_id, user.id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
