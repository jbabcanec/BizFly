from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import logging
from pathlib import Path

from core.config import settings
from api import health, businesses, templates, websites, research, preview, auth, preview_server, websites_list
from models.database import engine, Base
from services.preview_server import preview_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting BizFly application...")
    Base.metadata.create_all(bind=engine)
    # Start preview server manager
    await preview_manager.start()
    yield
    # Stop all preview servers on shutdown
    await preview_manager.stop()
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
app.include_router(websites_list.router, prefix="/api/websites", tags=["websites_list"])
app.include_router(preview_server.router, prefix="/api/websites", tags=["preview_server"])
app.include_router(websites.router, prefix="/api/websites", tags=["websites"])
app.include_router(preview.router, prefix="/preview", tags=["preview"])

# Mount static files for serving generated websites
static_path = Path("static")
if not static_path.exists():
    static_path.mkdir()
    
websites_path = static_path / "websites"
if not websites_path.exists():
    websites_path.mkdir()
    
images_path = static_path / "images"
if not images_path.exists():
    images_path.mkdir()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Preview route for generated websites
@app.get("/preview/{business_id}")
async def preview_website(business_id: str):
    """Preview a generated website"""
    website_path = Path(f"../generated_websites/{business_id}/index.html")
    if website_path.exists():
        with open(website_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="<h1>Website not found</h1>", status_code=404)