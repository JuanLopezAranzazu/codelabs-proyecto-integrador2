from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    created_at: datetime
    updated_at: datetime


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
