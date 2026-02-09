from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order import SalesOrder


def create(db: Session, order: SalesOrder) -> SalesOrder:
    db.add(order)
    db.flush()
    return order


def get_by_id(db: Session, order_id: int) -> SalesOrder | None:
    return db.scalar(select(SalesOrder).where(SalesOrder.id == order_id))


def get_by_id_for_update(db: Session, order_id: int) -> SalesOrder | None:
    stmt = select(SalesOrder).where(SalesOrder.id == order_id).with_for_update()
    return db.scalar(stmt)


def list_all(db: Session) -> list[SalesOrder]:
    return list(db.scalars(select(SalesOrder)))
