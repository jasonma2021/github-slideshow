from pydantic import BaseModel, condecimal

from app.core.constants import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: condecimal(max_digits=12, decimal_places=2)


class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemCreate]


class OrderItemOut(OrderItemCreate):
    id: int
    line_amount: condecimal(max_digits=12, decimal_places=2)

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    order_no: str
    customer_id: int
    status: OrderStatus
    total_amount: condecimal(max_digits=12, decimal_places=2)
    items: list[OrderItemOut]

    class Config:
        from_attributes = True
