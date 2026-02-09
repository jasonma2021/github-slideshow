from pydantic import BaseModel, condecimal

from app.core.constants import StockDocType


class StockInItem(BaseModel):
    product_id: int
    quantity: int
    unit_cost: condecimal(max_digits=12, decimal_places=2)


class StockInCreate(BaseModel):
    doc_no: str
    items: list[StockInItem]


class StockOutCreate(BaseModel):
    order_id: int


class StockDocumentOut(BaseModel):
    id: int
    doc_no: str
    doc_type: StockDocType
    related_order_id: int | None

    class Config:
        from_attributes = True
