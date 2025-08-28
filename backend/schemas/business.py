from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from models.business import WebsiteStatus


class BusinessSearch(BaseModel):
    location: str = Field(..., description="Location to search (address or coordinates)")
    radius_miles: float = Field(default=5.0, ge=0.1, le=50)
    business_types: Optional[List[str]] = None
    max_results: int = Field(default=60, ge=20, le=200, description="Maximum number of results to fetch")


class BusinessCreate(BaseModel):
    google_place_id: str
    name: str
    address: str
    latitude: float
    longitude: float
    phone: Optional[str] = None
    website: Optional[str] = None
    website_status: WebsiteStatus
    google_maps_url: Optional[str] = None
    business_type: Optional[str] = None


class BusinessResponse(BaseModel):
    id: UUID
    google_place_id: str
    name: str
    address: str
    latitude: float
    longitude: float
    phone: Optional[str]
    website: Optional[str]
    website_status: WebsiteStatus
    google_maps_url: Optional[str]
    business_type: Optional[str]
    discovered_at: datetime
    last_checked: datetime
    
    class Config:
        from_attributes = True


class BusinessFilter(BaseModel):
    website_status: Optional[WebsiteStatus] = None
    business_type: Optional[str] = None