from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Product
from .schemas import ProductCreate, ProductUpdate

from src.exceptions import NotFoundError


class ProductService:
    async def get_all_products(self, session: AsyncSession):
        result = await session.execute(select(Product).order_by(desc(Product.created_at)))
        return result.scalars().all()
    

    async def get_product_by_id(self, session: AsyncSession, product_id: int):
        result = await session.execute(select(Product).where(Product.id == product_id))
        db_product = result.scalar_one_or_none()

        if not db_product:
            raise NotFoundError(f"El producto con id {product_id} no existe")
        
        return db_product
    

    async def create_product(self, session: AsyncSession, product: ProductCreate):
        data = product.model_dump()
        db_product = Product(**data)
        session.add(db_product)
        
        await session.commit()
        await session.refresh(db_product)

        return db_product
    

    async def update_product(self, session: AsyncSession, product_id: int, product_update: ProductUpdate):
        db_product = await self.get_product_by_id(session, product_id)

        for key, value in product_update.dict(exclude_unset=True).items():
            setattr(db_product, key, value)

        await session.commit()
        await session.refresh(db_product)

        return db_product
    
    
    async def delete_product(self, session: AsyncSession, product_id: int):
        db_product = await self.get_product_by_id(session, product_id)
    
        await session.delete(db_product)
        await session.commit()
