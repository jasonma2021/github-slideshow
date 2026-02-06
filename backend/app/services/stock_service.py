from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.constants import StockDocType, OrderStatus, STOCK_OUT_PREFIX
from app.models.stock import StockBalance, StockDocument, StockLedger
from app.repositories import order_repo, stock_repo


def generate_stock_doc_no(prefix: str, now: datetime | None = None) -> str:
    timestamp = (now or datetime.utcnow()).strftime("%Y%m%d%H%M%S")
    return f"{prefix}{timestamp}"


def stock_in(db: Session, doc_no: str, items: list[dict], created_by: int) -> StockDocument:
    doc = StockDocument(doc_no=doc_no, doc_type=StockDocType.stock_in, created_by=created_by)
    stock_repo.create_document(db, doc)

    for item in items:
        balance = stock_repo.get_balance_for_update(db, item["product_id"])
        if not balance:
            balance = StockBalance(product_id=item["product_id"], quantity=0)
            stock_repo.create_balance(db, balance)
        balance.quantity += item["quantity"]
        ledger = StockLedger(
            stock_doc_id=doc.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_cost=item["unit_cost"],
            created_by=created_by,
        )
        stock_repo.create_ledger(db, ledger)

    return doc


def stock_out_for_order(db: Session, order_id: int, created_by: int) -> StockDocument:
    order = order_repo.get_by_id(db, order_id)
    if not order:
        raise ValueError("Order not found")
    if order.status == OrderStatus.shipped:
        raise ValueError("Order already shipped")

    doc = StockDocument(
        doc_no=generate_stock_doc_no(STOCK_OUT_PREFIX),
        doc_type=StockDocType.stock_out,
        related_order_id=order.id,
        created_by=created_by,
    )
    stock_repo.create_document(db, doc)

    for item in order.items:
        balance = stock_repo.get_balance_for_update(db, item.product_id)
        if not balance:
            raise ValueError("Stock balance not initialized")
        if balance.quantity < item.quantity:
            raise ValueError("Insufficient stock")
        balance.quantity -= item.quantity
        ledger = StockLedger(
            stock_doc_id=doc.id,
            product_id=item.product_id,
            quantity=-item.quantity,
            unit_cost=Decimal(str(item.unit_price)),
            created_by=created_by,
        )
        stock_repo.create_ledger(db, ledger)

    order.status = OrderStatus.shipped
    return doc
