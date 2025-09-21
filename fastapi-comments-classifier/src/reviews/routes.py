from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.db import get_session
from src.products.services import ProductService
from .services import ReviewService
from .schemas import Review, ReviewCreate, ReviewUpdate

product_service = ProductService()

review_router = APIRouter()
review_service = ReviewService(product_service=product_service)

# obtener reseñas
@review_router.get("/", response_model=List[Review], status_code=status.HTTP_200_OK)
async def get_reviews(
    session: AsyncSession = Depends(get_session),
):
    reviews = await review_service.get_all_reviews(session)
    return reviews

# obtener reseñas por su ID
@review_router.get("/{review_id}", response_model=Review, status_code=status.HTTP_200_OK)
async def get_review_by_id(
    review_id: int,
    session: AsyncSession = Depends(get_session),
):
    review = await review_service.get_review_by_id(session, review_id)
    return review

# crear nuevas reseñas
@review_router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    session: AsyncSession = Depends(get_session),
):
    created_review = await review_service.create_review(session, review)
    return created_review

# actualizar reseñas
@review_router.put("/{review_id}", response_model=Review, status_code=status.HTTP_200_OK)
async def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    session: AsyncSession = Depends(get_session)
):
    updated_review = await review_service.update_review(session, review_id, review_update)
    return updated_review
    
# eliminar reseñas
@review_router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    session: AsyncSession = Depends(get_session),
):
    await review_service.delete_review(session, review_id)
