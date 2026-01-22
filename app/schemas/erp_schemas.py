from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    role: Optional[str] = "operator"

class ProductCreate(BaseModel):
    name: str
    sku: str
    unit_price: float
    reorder_level: Optional[float] = 10.0
