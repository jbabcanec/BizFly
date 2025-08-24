from pydantic import BaseModel
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime


class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    thumbnail_url: Optional[str] = None
    preview_url: Optional[str] = None
    structure: Dict[str, Any]
    styles: Dict[str, Any]
    components: Dict[str, Any]


class TemplateResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    category: str
    thumbnail_url: Optional[str]
    preview_url: Optional[str]
    structure: Dict[str, Any]
    styles: Dict[str, Any]
    components: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True