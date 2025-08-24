from sqlalchemy import Column, String, Float, DateTime, Text, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from .database import Base


class WebsiteStatus(str, enum.Enum):
    NO_WEBSITE = "no_website"
    FACEBOOK_ONLY = "facebook_only"
    HAS_WEBSITE = "has_website"


class ResearchStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    google_place_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    phone = Column(String)
    website = Column(String)
    website_status = Column(Enum(WebsiteStatus), nullable=False)
    google_maps_url = Column(String)
    business_type = Column(String)
    
    discovered_at = Column(DateTime, default=datetime.utcnow)
    last_checked = Column(DateTime, default=datetime.utcnow)
    
    research = relationship("BusinessResearch", back_populates="business", uselist=False)
    generated_websites = relationship("GeneratedWebsite", back_populates="business")


class BusinessResearch(Base):
    __tablename__ = "business_research"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("businesses.id"), unique=True)
    
    status = Column(Enum(ResearchStatus), default=ResearchStatus.PENDING)
    
    description = Column(Text)
    services = Column(JSON)
    hours = Column(JSON)
    reviews = Column(JSON)
    social_media = Column(JSON)
    images = Column(JSON)
    menu_items = Column(JSON)
    specialties = Column(JSON)
    history = Column(Text)
    owner_info = Column(JSON)
    
    raw_research_data = Column(JSON)
    
    researched_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    business = relationship("Business", back_populates="research")