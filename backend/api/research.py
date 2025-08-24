from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from uuid import UUID

from models import get_db, Business, BusinessResearch, ResearchStatus
from agents.research_agent import ResearchAgent
from schemas.research import ResearchResponse, ResearchRequest

router = APIRouter()


@router.post("/{business_id}/start")
async def start_research(
    business_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> ResearchResponse:
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    existing_research = db.query(BusinessResearch).filter(
        BusinessResearch.business_id == business_id
    ).first()
    
    if existing_research and existing_research.status == ResearchStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Research already in progress")
    
    if not existing_research:
        research = BusinessResearch(
            business_id=business_id,
            status=ResearchStatus.IN_PROGRESS
        )
        db.add(research)
    else:
        existing_research.status = ResearchStatus.IN_PROGRESS
        research = existing_research
    
    db.commit()
    
    background_tasks.add_task(
        ResearchAgent().research_business,
        business_id=business_id
    )
    
    return ResearchResponse.from_orm(research)


@router.get("/{business_id}")
async def get_research(
    business_id: UUID,
    db: Session = Depends(get_db)
) -> ResearchResponse:
    research = db.query(BusinessResearch).filter(
        BusinessResearch.business_id == business_id
    ).first()
    
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    
    return ResearchResponse.from_orm(research)