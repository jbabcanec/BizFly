#!/usr/bin/env python3
"""
Seed script to initialize the database with default website templates.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base, get_db_url
from models.template import Template
from templates.template_manager import TemplateManager

def seed_templates():
    """Seed the database with default templates."""
    print("🌱 Seeding templates...")
    
    # Create database connection
    engine = create_engine(get_db_url())
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as session:
        # Check if templates already exist
        existing_count = session.query(Template).count()
        if existing_count > 0:
            print(f"⚡ Templates already exist ({existing_count} found). Skipping seed.")
            return
        
        # Get available templates from template manager
        template_manager = TemplateManager()
        available_templates = template_manager.get_available_templates()
        
        # Create template records
        for template_info in available_templates:
            template = Template(
                name=template_info['name'],
                description=template_info['description'],
                category=template_info.get('category', 'business'),
                is_active=True
            )
            session.add(template)
        
        session.commit()
        print(f"✅ Seeded {len(available_templates)} templates successfully!")

if __name__ == "__main__":
    try:
        seed_templates()
    except Exception as e:
        print(f"❌ Error seeding templates: {e}")
        sys.exit(1)