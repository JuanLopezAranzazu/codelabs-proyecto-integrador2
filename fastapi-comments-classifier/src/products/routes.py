from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.db import get_session
from .services import ProductService
from .schemas import Product, ProductCreate, ProductUpdate

product_router = APIRouter()
product_service = ProductService()

# obtener productos
@product_router.get("/", response_model=List[Product], status_code=status.HTTP_200_OK)
async def get_products(
    session: AsyncSession = Depends(get_session),
):
    products = await product_service.get_all_products(session)
    return products

# obtener productos por su ID
@product_router.get("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
async def get_product_by_id(
    product_id: int,
    session: AsyncSession = Depends(get_session),
):
    product = await product_service.get_product_by_id(session, product_id)
    return product

# crear nuevos productos
@product_router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    session: AsyncSession = Depends(get_session),
):
    created_product = await product_service.create_product(session, product)
    return created_product

# actualizar productos
@product_router.put("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: AsyncSession = Depends(get_session)
):
    updated_product = await product_service.update_product(session, product_id, product_update)
    return updated_product
    
# eliminar productos
@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
):
    await product_service.delete_product(session, product_id)
