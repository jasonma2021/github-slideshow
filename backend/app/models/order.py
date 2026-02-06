from sqlalchemy import ForeignKey, Numeric, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import OrderStatus
from app.models.base import Base


class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_no: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.created)
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2))
    created_by: Mapped[int] = mapped_column(index=True)

    items: Mapped[list["SalesOrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class SalesOrderItem(Base):
    __tablename__ = "sales_order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("sales_orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2))
    line_amount: Mapped[float] = mapped_column(Numeric(12, 2))

    order: Mapped[SalesOrder] = relationship(back_populates="items")
