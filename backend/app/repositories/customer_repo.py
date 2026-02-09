from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer


def create(db: Session, customer: Customer) -> Customer:
    db.add(customer)
    db.flush()
    return customer


def list_all(db: Session) -> list[Customer]:
    return list(db.scalars(select(Customer)))
