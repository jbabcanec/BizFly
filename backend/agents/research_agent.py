import anthropic
from typing import Dict, Any, List
from uuid import UUID
import logging
import json
from datetime import datetime

from core.config import settings
from models.database import SessionLocal
from models import Business, BusinessResearch, ResearchStatus

logger = logging.getLogger(__name__)


class ResearchAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    
    async def research_business(self, business_id: UUID):
        db = SessionLocal()
        try:
            business = db.query(Business).filter(Business.id == business_id).first()
            research = db.query(BusinessResearch).filter(
                BusinessResearch.business_id == business_id
            ).first()
            
            if not business or not research:
                logger.error(f"Business or research not found for {business_id}")
                return
            
            research_prompt = self._create_research_prompt(business)
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[{
                    "role": "user",
                    "content": research_prompt
                }]
            )
            
            research_data = self._parse_research_response(response.content[0].text)
            
            research.description = research_data.get("description")
            research.services = research_data.get("services", [])
            research.hours = research_data.get("hours", {})
            research.reviews = research_data.get("reviews", [])
            research.social_media = research_data.get("social_media", {})
            research.images = research_data.get("images", [])
            research.menu_items = research_data.get("menu_items", [])
            research.specialties = research_data.get("specialties", [])
            research.history = research_data.get("history")
            research.owner_info = research_data.get("owner_info", {})
            research.raw_research_data = research_data
            research.status = ResearchStatus.COMPLETED
            research.researched_at = datetime.utcnow()
            
            db.commit()
            
            logger.info(f"Research completed for {business.name}")
            
        except Exception as e:
            logger.error(f"Research failed: {e}")
            if research:
                research.status = ResearchStatus.FAILED
                db.commit()
        finally:
            db.close()
    
    def _create_research_prompt(self, business: Business) -> str:
        return f"""Research the following business and provide detailed information:

Business Name: {business.name}
Address: {business.address}
Phone: {business.phone or 'Not available'}
Current Website: {business.website or 'None'}
Google Maps URL: {business.google_maps_url or 'Not available'}

Please research and provide the following information in JSON format:
1. A compelling business description (2-3 sentences)
2. List of services offered
3. Business hours
4. Recent reviews or testimonials (if available)
5. Social media presence
6. Suggested images (descriptions of what would work)
7. Menu items or product offerings (if applicable)
8. Specialties or unique selling points
9. Brief history (if available)
10. Owner information (if publicly available)

Return the information as a valid JSON object with these keys:
- description: string
- services: array of strings
- hours: object with day names as keys
- reviews: array of review objects
- social_media: object with platform names as keys
- images: array of image description strings
- menu_items: array of item objects
- specialties: array of strings
- history: string
- owner_info: object

If information is not available for any field, use appropriate empty values."""
    
    def _parse_research_response(self, response: str) -> Dict[str, Any]:
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "{" in response:
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                json_str = response
            
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to parse research response: {e}")
            return {
                "description": response[:500] if len(response) > 500 else response,
                "services": [],
                "hours": {},
                "reviews": [],
                "social_media": {},
                "images": [],
                "menu_items": [],
                "specialties": [],
                "history": "",
                "owner_info": {}
            }