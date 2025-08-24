from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path

router = APIRouter()

GENERATED_WEBSITES_DIR = Path("../generated_websites")


@router.get("/{business_id}")
async def preview_website(business_id: str) -> HTMLResponse:
    website_dir = GENERATED_WEBSITES_DIR / business_id
    index_file = website_dir / "index.html"
    
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Website not found")
    
    content = index_file.read_text(encoding='utf-8')
    return HTMLResponse(content=content)


@router.get("/{business_id}/{file_path:path}")
async def get_website_asset(business_id: str, file_path: str):
    website_dir = GENERATED_WEBSITES_DIR / business_id
    asset_file = website_dir / file_path
    
    if not asset_file.exists() or not asset_file.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(asset_file)