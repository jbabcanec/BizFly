from pydantic import BaseModel
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime


class WebsiteCreate(BaseModel):
    business_id: UUID
    template_id: UUID
    settings: Optional[Dict[str, Any]] = None


class WebsiteUpdate(BaseModel):
    content: Optional[Dict[str, Any]] = None
    settings: Optional[Dict[str, Any]] = None
    is_published: Optional[bool] = None
    custom_domain: Optional[str] = None


class WebsiteResponse(BaseModel):
    id: UUID
    business_id: UUID
    template_id: UUID
    subdomain: Optional[str]
    custom_domain: Optional[str]
    content: Dict[str, Any]
    settings: Optional[Dict[str, Any]]
    is_published: bool
    published_at: Optional[datetime]
    preview_url: Optional[str]
    production_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True