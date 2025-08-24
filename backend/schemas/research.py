from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from uuid import UUID
from datetime import datetime

from models.business import ResearchStatus


class ResearchRequest(BaseModel):
    force_refresh: bool = False


class ResearchResponse(BaseModel):
    id: UUID
    business_id: UUID
    status: ResearchStatus
    description: Optional[str]
    services: Optional[List[str]]
    hours: Optional[Dict[str, str]]
    reviews: Optional[List[Dict[str, Any]]]
    social_media: Optional[Dict[str, str]]
    images: Optional[List[str]]
    menu_items: Optional[List[Dict[str, Any]]]
    specialties: Optional[List[str]]
    history: Optional[str]
    owner_info: Optional[Dict[str, Any]]
    researched_at: Optional[datetime]
    updated_at: datetime
    
    class Config:
        from_attributes = True