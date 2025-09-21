from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Review(BaseModel):
    id: int
    product_id: int
    review_text: str
    sentiment: str
    created_at: datetime
    updated_at: datetime


class ReviewCreate(BaseModel):
    product_id: int
    review_text: str


class ReviewUpdate(BaseModel):
    product_id: Optional[int] = None
    review_text: Optional[str] = None
