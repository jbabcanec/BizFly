from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from models import get_db, Business
from services.google_places import GooglePlacesService
from schemas.business import (
    BusinessSearch, 
    BusinessResponse, 
    BusinessCreate,
    BusinessFilter
)

router = APIRouter()


@router.post("/search")
async def search_businesses(
    search: BusinessSearch,
    db: Session = Depends(get_db)
) -> List[BusinessResponse]:
    places_service = GooglePlacesService()
    
    try:
        businesses = await places_service.search_businesses(
            location=search.location,
            radius_miles=search.radius_miles,
            business_types=search.business_types
        )
        
        for business_data in businesses:
            existing = db.query(Business).filter_by(
                google_place_id=business_data['place_id']
            ).first()
            
            if not existing:
                new_business = Business(
                    google_place_id=business_data['place_id'],
                    name=business_data['name'],
                    address=business_data['address'],
                    latitude=business_data['latitude'],
                    longitude=business_data['longitude'],
                    phone=business_data.get('phone'),
                    website=business_data.get('website'),
                    website_status=business_data['website_status'],
                    google_maps_url=business_data.get('google_maps_url'),
                    business_type=business_data.get('business_type')
                )
                db.add(new_business)
        
        db.commit()
        
        return [BusinessResponse.from_orm(b) for b in businesses]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_businesses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    website_status: Optional[str] = None,
    db: Session = Depends(get_db)
) -> List[BusinessResponse]:
    query = db.query(Business)
    
    if website_status:
        query = query.filter(Business.website_status == website_status)
    
    businesses = query.offset(skip).limit(limit).all()
    return [BusinessResponse.from_orm(b) for b in businesses]


@router.get("/{business_id}")
async def get_business(
    business_id: UUID,
    db: Session = Depends(get_db)
) -> BusinessResponse:
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    return BusinessResponse.from_orm(business)