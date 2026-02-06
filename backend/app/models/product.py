from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2))
    created_by: Mapped[int] = mapped_column(index=True)
