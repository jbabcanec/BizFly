from sqlalchemy import Column, String, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .database import Base


class Template(Base):
    __tablename__ = "templates"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    category = Column(String, nullable=False)
    
    thumbnail_url = Column(String)
    preview_url = Column(String)
    
    structure = Column(JSON, nullable=False)
    styles = Column(JSON, nullable=False)
    components = Column(JSON, nullable=False)
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    generated_websites = relationship("GeneratedWebsite", back_populates="template")


class GeneratedWebsite(Base):
    __tablename__ = "generated_websites"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    template_id = Column(String, ForeignKey("templates.id"), nullable=False)
    
    subdomain = Column(String, unique=True)
    custom_domain = Column(String, unique=True)
    
    content = Column(JSON, nullable=False)
    settings = Column(JSON)
    
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime)
    
    preview_url = Column(String)
    production_url = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    business = relationship("Business", back_populates="generated_websites")
    template = relationship("Template", back_populates="generated_websites")