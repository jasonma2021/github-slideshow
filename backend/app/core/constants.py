from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    staff = "staff"


class OrderStatus(str, Enum):
    created = "created"
    confirmed = "confirmed"
    shipped = "shipped"
    cancelled = "cancelled"


class StockDocType(str, Enum):
    stock_in = "stock_in"
    stock_out = "stock_out"


ORDER_NO_PREFIX = "SO"
STOCK_OUT_PREFIX = "SO"
