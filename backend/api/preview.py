from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from uuid import UUID

router = APIRouter()

GENERATED_WEBSITES_DIR = Path("generated_websites")


@router.get("/{website_id}")
async def preview_website(website_id: UUID) -> HTMLResponse:
    website_dir = GENERATED_WEBSITES_DIR / str(website_id)
    index_file = website_dir / "index.html"
    
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Website not found")
    
    content = index_file.read_text(encoding='utf-8')
    return HTMLResponse(content=content)


@router.get("/{website_id}/{file_path:path}")
async def get_website_asset(website_id: UUID, file_path: str):
    website_dir = GENERATED_WEBSITES_DIR / str(website_id)
    asset_file = website_dir / file_path
    
    if not asset_file.exists() or not asset_file.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(asset_file)