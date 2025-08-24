#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from models.database import SessionLocal, engine, Base
from models.template import Template
from templates.template_manager import TemplateManager


def seed_templates():
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        template_manager = TemplateManager()
        
        for template_id, template_obj in template_manager.templates.items():
            existing = db.query(Template).filter_by(name=template_obj.name).first()
            if existing:
                print(f"Template '{template_obj.name}' already exists, skipping")
                continue
            
            new_template = Template(
                name=template_obj.name,
                description=f"Professional {template_obj.name.lower()} template for business websites",
                category=template_obj.category,
                thumbnail_url=f"/templates/{template_id}/thumbnail.jpg",
                preview_url=f"/templates/{template_id}/preview",
                structure=template_obj.get_structure(),
                styles=template_obj.get_styles(),
                components={}
            )
            
            db.add(new_template)
            print(f"Added template: {template_obj.name}")
        
        db.commit()
        print("Template seeding completed successfully")
        
    except Exception as e:
        print(f"Error seeding templates: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_templates()