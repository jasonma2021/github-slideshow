from fastapi import FastAPI

from app.api.routers import auth, customers, orders, products, reports, stock, users
from app.core.config import settings
from app.core.database import engine
from app.models import customer, order, product, stock, user  # noqa: F401
from app.models.base import Base

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(users.router, prefix=settings.api_v1_prefix)
app.include_router(customers.router, prefix=settings.api_v1_prefix)
app.include_router(products.router, prefix=settings.api_v1_prefix)
app.include_router(orders.router, prefix=settings.api_v1_prefix)
app.include_router(stock.router, prefix=settings.api_v1_prefix)
app.include_router(reports.router, prefix=settings.api_v1_prefix)
