from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import DateTime

class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))

    reviews: List["Review"] = Relationship(back_populates="product")

    def __repr__(self):
        return f"Product(name={self.name}, description={self.description}, price={self.price})"
    

class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id") 
    review_text: str
    sentiment: str
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime))

    product: Optional[Product] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"Review(review_text={self.review_text}, sentiment={self.sentiment})"
    