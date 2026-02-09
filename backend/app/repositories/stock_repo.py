from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.stock import StockBalance, StockDocument, StockLedger


def get_balance_for_update(db: Session, product_id: int) -> StockBalance | None:
    stmt = select(StockBalance).where(StockBalance.product_id == product_id).with_for_update()
    return db.scalar(stmt)


def create_balance(db: Session, balance: StockBalance) -> StockBalance:
    db.add(balance)
    db.flush()
    return balance


def create_document(db: Session, doc: StockDocument) -> StockDocument:
    db.add(doc)
    db.flush()
    return doc


def create_ledger(db: Session, ledger: StockLedger) -> StockLedger:
    db.add(ledger)
    db.flush()
    return ledger
