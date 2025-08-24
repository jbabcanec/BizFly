from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from models import get_db, Template
from schemas.template import TemplateResponse, TemplateCreate

router = APIRouter()


@router.get("/")
async def list_templates(
    db: Session = Depends(get_db)
) -> List[TemplateResponse]:
    templates = db.query(Template).filter(Template.is_active == True).all()
    return [TemplateResponse.from_orm(t) for t in templates]


@router.get("/{template_id}")
async def get_template(
    template_id: UUID,
    db: Session = Depends(get_db)
) -> TemplateResponse:
    template = db.query(Template).filter(Template.id == template_id).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return TemplateResponse.from_orm(template)


@router.get("/category/{category}")
async def get_templates_by_category(
    category: str,
    db: Session = Depends(get_db)
) -> List[TemplateResponse]:
    templates = db.query(Template).filter(
        Template.category == category,
        Template.is_active == True
    ).all()
    
    return [TemplateResponse.from_orm(t) for t in templates]