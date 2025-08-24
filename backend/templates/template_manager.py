from typing import Dict, Any, Optional, List
from pathlib import Path
import json
from .minimal_template import MinimalTemplate
from .modern_template import ModernTemplate
from .luxury_template import LuxuryTemplate
from .base_template import BaseTemplate


class TemplateManager:
    def __init__(self):
        self.templates: Dict[str, BaseTemplate] = {
            "minimal": MinimalTemplate(),
            "modern": ModernTemplate(),
            "luxury": LuxuryTemplate()
        }
        self.output_base = Path("generated_websites")
    
    def get_template(self, template_name: str) -> Optional[BaseTemplate]:
        return self.templates.get(template_name)
    
    def list_templates(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": key,
                "name": template.name,
                "category": template.category,
                "structure": template.get_structure(),
                "styles": template.get_styles()
            }
            for key, template in self.templates.items()
        ]
    
    def generate_website(
        self,
        template_name: str,
        business_data: Dict[str, Any],
        website_id: str
    ) -> Dict[str, Any]:
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        html_content = template.render(business_data)
        
        output_dir = self.output_base / website_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        index_path = output_dir / "index.html"
        template.save_to_file(html_content, index_path)
        
        metadata_path = output_dir / "metadata.json"
        metadata = {
            "template": template_name,
            "business_name": business_data.get("business", {}).get("name"),
            "generated_files": ["index.html"]
        }
        metadata_path.write_text(json.dumps(metadata, indent=2))
        
        return {
            "success": True,
            "output_dir": str(output_dir),
            "files": ["index.html", "metadata.json"],
            "preview_url": f"/preview/{website_id}"
        }
    
    def get_template_preview(self, template_name: str) -> str:
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        sample_data = {
            "business": {
                "name": "Sample Business",
                "address": "123 Main Street, City, State 12345",
                "phone": "(555) 123-4567"
            },
            "description": "This is a sample business description showcasing the template design.",
            "services": ["Service One", "Service Two", "Service Three"],
            "hours": {
                "Monday": "9:00 AM - 5:00 PM",
                "Tuesday": "9:00 AM - 5:00 PM",
                "Wednesday": "9:00 AM - 5:00 PM",
                "Thursday": "9:00 AM - 5:00 PM",
                "Friday": "9:00 AM - 5:00 PM",
                "Saturday": "10:00 AM - 3:00 PM",
                "Sunday": "Closed"
            }
        }
        
        return template.render(sample_data)