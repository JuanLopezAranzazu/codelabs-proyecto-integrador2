from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.db.db import init_db, get_session

from src.products.routes import product_router
from src.reviews.routes import review_router

from .middlewares import ExceptionHandlerMiddleware

version = "v1"

description = """
FastAPI + NLP Clasificación de comentarios.
"""

version_prefix =f"/api/{version}"

app = FastAPI(
  title="API REST demo",
  description=description,
  version=version,
  openapi_url=f"{version_prefix}/openapi.json",
  docs_url=f"{version_prefix}/docs",
  redoc_url=f"{version_prefix}/redoc"
)

app.add_middleware(ExceptionHandlerMiddleware)

# verificar la API
@app.get(version_prefix + "/")
async def root():
    """
    Verificar que la API está funcionando.
    """
    return {"message": "Bienvenido a la API!"}


# verificar conexion con la db
@app.get(version_prefix + "/ping")
async def ping(session: AsyncSession = Depends(get_session)):
    """
    Verificar que la conexión a la base de datos está funcionando.
    """
    result = await session.execute(text("SELECT 1"))
    return {result}


# Rutas de la API
app.include_router(product_router, prefix=version_prefix + "/products", tags=["products"])
app.include_router(review_router, prefix=version_prefix + "/reviews", tags=["reviews"])

# ----------------------------
# Evento startup para inicializar DB
# ----------------------------
@app.on_event("startup")
async def on_startup():
    await init_db()  # crea todas las tablas si no existen
