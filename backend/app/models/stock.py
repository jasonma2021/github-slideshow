from sqlalchemy import ForeignKey, Numeric, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import StockDocType
from app.models.base import Base


class StockBalance(Base):
    __tablename__ = "stock_balances"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), unique=True)
    quantity: Mapped[int] = mapped_column(default=0)


class StockDocument(Base):
    __tablename__ = "stock_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    doc_no: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    doc_type: Mapped[StockDocType] = mapped_column(Enum(StockDocType))
    related_order_id: Mapped[int | None] = mapped_column(
        ForeignKey("sales_orders.id"), nullable=True
    )
    created_by: Mapped[int] = mapped_column(index=True)


class StockLedger(Base):
    __tablename__ = "stock_ledgers"

    id: Mapped[int] = mapped_column(primary_key=True)
    stock_doc_id: Mapped[int] = mapped_column(ForeignKey("stock_documents.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()
    unit_cost: Mapped[float] = mapped_column(Numeric(12, 2))
    created_by: Mapped[int] = mapped_column(index=True)
