from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
import joblib

from src.db.models import Product, Review
from .schemas import ReviewCreate, ReviewUpdate

from src.exceptions import NotFoundError

from src.ml.utils import predict_sentiment


class ReviewService:
    def __init__(self, product_service):
        self.product_service = product_service
        # cargar modelo y vectorizer al iniciar el servicio
        self.vectorizer = joblib.load("tfidf_vectorizer.joblib")
        self.model = joblib.load("sentiment_model.joblib")

    async def get_all_reviews(self, session: AsyncSession):
        result = await session.execute(select(Review).order_by(desc(Review.created_at)))
        return result.scalars().all()
    

    async def get_review_by_id(self, session: AsyncSession, review_id: int):
        result = await session.execute(select(Review).where(Review.id == review_id))
        db_review = result.scalar_one_or_none()

        if not db_review:
            raise NotFoundError(f"La reseña con id {review_id} no existe")
        
        return db_review
    

    async def create_review(self, session: AsyncSession, review: ReviewCreate):
        # verificar el producto
        await self.product_service.get_product_by_id(session, review.product_id)

        # predecir sentimiento usando la función modular
        sentiment = predict_sentiment(self.model, self.vectorizer, review.review_text)

        data = review.model_dump()
        data["sentiment"] = sentiment
        db_review = Review(**data)

        session.add(db_review)
        await session.commit()
        await session.refresh(db_review)

        return db_review
    

    async def update_review(self, session: AsyncSession, review_id: int, review_update: ReviewUpdate):
        db_review = await self.get_review_by_id(session, review_id)

        # verificar el producto
        if "product_id" in review_update.dict(exclude_unset=True):
            await self.product_service.get_product_by_id(session, review_update.product_id)

        # recalcular el sentimiento automáticamente
        if "review_text" in review_update.dict(exclude_unset=True):
            db_review.sentiment = predict_sentiment(self.model, self.vectorizer, db_review.review_text)


        for key, value in review_update.dict(exclude_unset=True).items():
            setattr(db_review, key, value)


        await session.commit()
        await session.refresh(db_review)

        return db_review
    
    
    async def delete_review(self, session: AsyncSession, review_id: int):
        db_review = await self.get_review_by_id(session, review_id)
    
        await session.delete(db_review)
        await session.commit()
