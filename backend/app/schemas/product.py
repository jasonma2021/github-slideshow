from pydantic import BaseModel, condecimal


class ProductCreate(BaseModel):
    name: str
    sku: str
    unit_price: condecimal(max_digits=12, decimal_places=2)


class ProductOut(ProductCreate):
    id: int

    class Config:
        from_attributes = True
