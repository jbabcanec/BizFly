from typing import Dict, Any
from uuid import UUID
import logging
import json
from pathlib import Path

from models.database import SessionLocal
from models import GeneratedWebsite, Business, Template, BusinessResearch
from templates.template_manager import TemplateManager

logger = logging.getLogger(__name__)


class WebsiteGenerator:
    def __init__(self):
        self.output_dir = Path("generated_websites")
        self.output_dir.mkdir(exist_ok=True)
        self.template_manager = TemplateManager()
    
    async def generate(self, website_id: UUID):
        db = SessionLocal()
        try:
            website = db.query(GeneratedWebsite).filter(
                GeneratedWebsite.id == website_id
            ).first()
            
            if not website:
                logger.error(f"Website {website_id} not found")
                return
            
            business = db.query(Business).filter(
                Business.id == website.business_id
            ).first()
            
            template = db.query(Template).filter(
                Template.id == website.template_id
            ).first()
            
            research = db.query(BusinessResearch).filter(
                BusinessResearch.business_id == website.business_id
            ).first()
            
            content = self._generate_content(business, research)
            
            template_name = template.name.lower() if template else "minimal"
            result = self.template_manager.generate_website(
                template_name=template_name,
                business_data=content,
                website_id=str(website.id)
            )
            
            website.content = content
            website.preview_url = result["preview_url"]
            
            db.commit()
            
            logger.info(f"Website generated successfully for {business.name}")
            
        except Exception as e:
            logger.error(f"Failed to generate website: {e}")
            db.rollback()
        finally:
            db.close()
    
    def _generate_content(
        self, 
        business: Business, 
        research: BusinessResearch
    ) -> Dict[str, Any]:
        content = {
            "business": {
                "name": business.name,
                "address": business.address,
                "phone": business.phone,
                "location": {
                    "lat": business.latitude,
                    "lng": business.longitude
                }
            }
        }
        
        if research and research.status == "completed":
            content.update({
                "description": research.description,
                "services": research.services or [],
                "hours": research.hours or {},
                "reviews": research.reviews or [],
                "images": research.images or [],
                "specialties": research.specialties or [],
                "history": research.history
            })
        
        return content