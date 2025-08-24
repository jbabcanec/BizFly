"""
Preview Server API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
from services.preview_server import PreviewServerAPI, preview_manager
from api.auth import get_current_user

router = APIRouter()


@router.post("/{business_id}/preview")
async def start_preview(business_id: str, current_user: str = Depends(get_current_user)):
    """Start a preview server for a business website"""
    result = await PreviewServerAPI.start_preview(business_id)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.delete("/{business_id}/preview")
async def stop_preview(business_id: str, current_user: str = Depends(get_current_user)):
    """Stop a preview server"""
    result = PreviewServerAPI.stop_preview(business_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/{business_id}/preview/status")
async def get_preview_status(business_id: str, current_user: str = Depends(get_current_user)):
    """Get preview server status"""
    result = PreviewServerAPI.get_preview_status(business_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/previews")
async def list_all_previews(current_user: str = Depends(get_current_user)):
    """List all active preview servers"""
    return PreviewServerAPI.list_all_previews()


@router.get("/{business_id}/download")
async def download_website(business_id: str, current_user: str = Depends(get_current_user)):
    """Download website as ZIP"""
    from services.website_storage import WebsiteStorage
    from fastapi.responses import FileResponse
    
    storage = WebsiteStorage()
    zip_path = storage.create_zip_bundle(business_id)
    
    if not zip_path:
        raise HTTPException(status_code=404, detail="Website not found")
    
    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename=f"{business_id}_website.zip"
    )