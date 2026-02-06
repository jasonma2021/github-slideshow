from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.constants import OrderStatus, ORDER_NO_PREFIX
from app.models.order import SalesOrder, SalesOrderItem
from app.repositories import order_repo, product_repo


def generate_order_no(prefix: str, now: datetime | None = None) -> str:
    timestamp = (now or datetime.utcnow()).strftime("%Y%m%d%H%M%S")
    return f"{prefix}{timestamp}"


def create_order(db: Session, customer_id: int, items: list[dict], created_by: int) -> SalesOrder:
    order_items: list[SalesOrderItem] = []
    total_amount = Decimal("0.00")

    for item in items:
        product = product_repo.get_by_id(db, item["product_id"])
        if not product:
            raise ValueError("Product not found")
        line_amount = Decimal(str(item["unit_price"])) * Decimal(item["quantity"])
        order_items.append(
            SalesOrderItem(
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                line_amount=line_amount,
            )
        )
        total_amount += line_amount

    order = SalesOrder(
        order_no=generate_order_no(ORDER_NO_PREFIX),
        customer_id=customer_id,
        status=OrderStatus.created,
        total_amount=total_amount,
        created_by=created_by,
        items=order_items,
    )
    return order_repo.create(db, order)
