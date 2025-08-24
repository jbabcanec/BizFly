"""
API endpoint for listing generated websites
"""
from fastapi import APIRouter, Depends
from typing import List, Dict
import json
from pathlib import Path
from datetime import datetime
from api.auth import get_current_user
from services.website_storage import WebsiteStorage

router = APIRouter()

@router.get("/list")
async def list_websites(current_user: str = Depends(get_current_user)) -> Dict:
    """List all generated websites"""
    
    storage = WebsiteStorage()
    websites_dir = Path("../generated_websites")
    
    websites = []
    
    if websites_dir.exists():
        for website_dir in websites_dir.iterdir():
            if website_dir.is_dir():
                metadata_path = website_dir / "metadata.json"
                
                if metadata_path.exists():
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                        
                        # Generate thumbnail from business type or use placeholder
                        business_type = metadata.get('business_type', 'business')
                        thumbnail = f"https://picsum.photos/seed/{website_dir.name}/400/300"
                        
                        # Calculate folder size
                        size = sum(f.stat().st_size for f in website_dir.rglob('*') if f.is_file())
                        size_mb = size / (1024 * 1024)
                        
                        website_data = {
                            "id": website_dir.name,
                            "businessName": metadata.get("business_name", website_dir.name.replace("_", " ").title()),
                            "businessId": metadata.get("business_id", website_dir.name),
                            "template": metadata.get("template", "Unknown"),
                            "generatedAt": metadata.get("generated_at", datetime.now().isoformat()),
                            "lastModified": datetime.fromtimestamp(website_dir.stat().st_mtime).isoformat(),
                            "status": metadata.get("status", "draft"),
                            "thumbnail": thumbnail,
                            "size": f"{size_mb:.1f} MB",
                            "description": metadata.get("description", ""),
                            "features": metadata.get("features", [])
                        }
                        
                        websites.append(website_data)
                        
                    except Exception as e:
                        print(f"Error reading metadata for {website_dir.name}: {e}")
    
    # Sort by last modified (newest first)
    websites.sort(key=lambda x: x["lastModified"], reverse=True)
    
    return {
        "success": True,
        "websites": websites,
        "count": len(websites)
    }