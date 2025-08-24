from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from core.config import settings
from api import health, businesses, templates, websites, research, preview, auth
from models.database import engine, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting BizFly application...")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down BizFly application...")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(businesses.router, prefix="/api/businesses", tags=["businesses"])
app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
app.include_router(websites.router, prefix="/api/websites", tags=["websites"])
app.include_router(preview.router, prefix="/preview", tags=["preview"])