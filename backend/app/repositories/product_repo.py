from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


def create(db: Session, product: Product) -> Product:
    db.add(product)
    db.flush()
    return product


def list_all(db: Session) -> list[Product]:
    return list(db.scalars(select(Product)))


def get_by_id(db: Session, product_id: int) -> Product | None:
    return db.scalar(select(Product).where(Product.id == product_id))
