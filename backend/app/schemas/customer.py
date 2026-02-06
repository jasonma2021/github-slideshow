from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    contact_name: str
    contact_phone: str
    address: str


class CustomerOut(CustomerCreate):
    id: int

    class Config:
        from_attributes = True
