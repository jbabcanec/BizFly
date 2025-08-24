import pytest
from pathlib import Path
import json
import tempfile
import shutil

from templates.template_manager import TemplateManager


@pytest.fixture
def template_manager():
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = TemplateManager()
        manager.output_base = Path(temp_dir)
        yield manager


@pytest.mark.unit
def test_get_template(template_manager: TemplateManager):
    template = template_manager.get_template("minimal")
    assert template is not None
    assert template.name == "Minimal"
    assert template.category == "universal"


@pytest.mark.unit
def test_get_nonexistent_template(template_manager: TemplateManager):
    template = template_manager.get_template("nonexistent")
    assert template is None


@pytest.mark.unit
def test_list_templates(template_manager: TemplateManager):
    templates = template_manager.list_templates()
    assert len(templates) >= 2
    
    template_names = [t["name"] for t in templates]
    assert "Minimal" in template_names
    assert "Modern" in template_names


@pytest.mark.unit
def test_generate_website(template_manager: TemplateManager):
    business_data = {
        "business": {
            "name": "Test Business",
            "address": "123 Test St",
            "phone": "(555) 123-4567"
        },
        "description": "A test business",
        "services": ["Service 1", "Service 2"]
    }
    
    website_id = "test-website-123"
    
    result = template_manager.generate_website(
        template_name="minimal",
        business_data=business_data,
        website_id=website_id
    )
    
    assert result["success"] is True
    assert "index.html" in result["files"]
    assert "metadata.json" in result["files"]
    
    # Check files exist
    output_dir = Path(result["output_dir"])
    assert (output_dir / "index.html").exists()
    assert (output_dir / "metadata.json").exists()
    
    # Check HTML content
    html_content = (output_dir / "index.html").read_text()
    assert "Test Business" in html_content
    assert "(555) 123-4567" in html_content
    
    # Check metadata
    metadata = json.loads((output_dir / "metadata.json").read_text())
    assert metadata["template"] == "minimal"
    assert metadata["business_name"] == "Test Business"


@pytest.mark.unit
def test_get_template_preview(template_manager: TemplateManager):
    preview_html = template_manager.get_template_preview("minimal")
    assert "Sample Business" in preview_html
    assert "(555) 123-4567" in preview_html
    assert "DOCTYPE html" in preview_html