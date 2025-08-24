from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from models import get_db, GeneratedWebsite, Business, Template
from schemas.website import WebsiteCreate, WebsiteResponse, WebsiteUpdate
from services.website_generator import WebsiteGenerator

router = APIRouter()


@router.post("/generate")
async def generate_website(
    website_data: WebsiteCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> WebsiteResponse:
    business = db.query(Business).filter(Business.id == website_data.business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    template = db.query(Template).filter(Template.id == website_data.template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    website = GeneratedWebsite(
        business_id=website_data.business_id,
        template_id=website_data.template_id,
        content={},
        settings=website_data.settings or {}
    )
    
    db.add(website)
    db.commit()
    db.refresh(website)
    
    background_tasks.add_task(
        WebsiteGenerator().generate,
        website_id=website.id
    )
    
    return WebsiteResponse.from_orm(website)


@router.get("/{website_id}")
async def get_website(
    website_id: UUID,
    db: Session = Depends(get_db)
) -> WebsiteResponse:
    website = db.query(GeneratedWebsite).filter(
        GeneratedWebsite.id == website_id
    ).first()
    
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    return WebsiteResponse.from_orm(website)


@router.get("/business/{business_id}")
async def get_business_websites(
    business_id: UUID,
    db: Session = Depends(get_db)
) -> List[WebsiteResponse]:
    websites = db.query(GeneratedWebsite).filter(
        GeneratedWebsite.business_id == business_id
    ).all()
    
    return [WebsiteResponse.from_orm(w) for w in websites]


@router.patch("/{website_id}")
async def update_website(
    website_id: UUID,
    update_data: WebsiteUpdate,
    db: Session = Depends(get_db)
) -> WebsiteResponse:
    website = db.query(GeneratedWebsite).filter(
        GeneratedWebsite.id == website_id
    ).first()
    
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    if update_data.content:
        website.content = update_data.content
    if update_data.settings:
        website.settings = update_data.settings
    if update_data.is_published is not None:
        website.is_published = update_data.is_published
    
    db.commit()
    db.refresh(website)
    
    return WebsiteResponse.from_orm(website)