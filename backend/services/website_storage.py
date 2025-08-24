"""
Website Storage System - How BizFly stores and serves generated websites
"""
import os
import json
import shutil
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import hashlib
import logging

logger = logging.getLogger(__name__)


class WebsiteStorage:
    """
    Manages storage and serving of generated websites
    
    Storage Structure:
    generated_websites/
    ├── business_id_1/
    │   ├── index.html
    │   ├── styles.css
    │   ├── script.js
    │   ├── images/
    │   │   ├── hero.jpg
    │   │   ├── gallery_1.jpg
    │   │   └── logo.svg
    │   └── metadata.json
    ├── business_id_2/
    │   └── ...
    └── templates/
        └── shared_assets/
    """
    
    def __init__(self, base_path: str = "../generated_websites"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        
        # Create shared assets directory
        self.shared_assets = self.base_path / "templates" / "shared_assets"
        self.shared_assets.mkdir(parents=True, exist_ok=True)
        
        # Static file server path (for FastAPI)
        self.static_path = Path("static/websites")
        self.static_path.mkdir(parents=True, exist_ok=True)
    
    def save_website(
        self, 
        business_id: str,
        html: str,
        css: str = "",
        js: str = "",
        images: Dict[str, str] = None,
        metadata: Dict = None
    ) -> Dict[str, str]:
        """
        Save a complete website to disk
        
        Returns:
            Dict with URLs to access the website
        """
        # Create business directory
        website_dir = self.base_path / business_id
        website_dir.mkdir(exist_ok=True)
        
        # Save HTML
        html_path = website_dir / "index.html"
        html = self._inject_local_assets(html, business_id)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Save CSS
        if css:
            css_path = website_dir / "styles.css"
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css)
        
        # Save JavaScript
        if js:
            js_path = website_dir / "script.js"
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(js)
        
        # Handle images
        if images:
            self._save_images(website_dir, images)
        
        # Save metadata
        metadata = metadata or {}
        metadata.update({
            "business_id": business_id,
            "generated_at": datetime.utcnow().isoformat(),
            "version": "1.0",
            "files": {
                "html": "index.html",
                "css": "styles.css" if css else None,
                "js": "script.js" if js else None
            }
        })
        
        metadata_path = website_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Create symlink for static serving
        static_link = self.static_path / business_id
        if static_link.exists():
            static_link.unlink()
        static_link.symlink_to(website_dir.absolute())
        
        return {
            "preview_url": f"/preview/{business_id}",
            "static_url": f"/static/websites/{business_id}/",
            "download_url": f"/api/websites/{business_id}/download",
            "edit_url": f"/editor/{business_id}"
        }
    
    def _inject_local_assets(self, html: str, business_id: str) -> str:
        """Modify HTML to use local assets instead of external URLs"""
        
        # Replace external image URLs with local paths
        replacements = {
            'src="https://picsum.photos': f'src="/static/websites/{business_id}/images',
            'src="https://ui-avatars.com': f'src="/static/websites/{business_id}/images/logo.svg',
            'href="styles.css"': f'href="/static/websites/{business_id}/styles.css"',
            'src="script.js"': f'src="/static/websites/{business_id}/script.js"'
        }
        
        for old, new in replacements.items():
            html = html.replace(old, new)
        
        return html
    
    def _save_images(self, website_dir: Path, images):
        """Download and save images locally"""
        images_dir = website_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        # Handle different image formats
        if isinstance(images, dict):
            for name, url in images.items():
                self._download_image(images_dir, name, url)
        
    def _download_image(self, images_dir: Path, name: str, url):
        """Download a single image"""
        if isinstance(url, list):
            # Handle gallery arrays
            for i, img_url in enumerate(url):
                self._download_single_image(images_dir, f"{name}_{i}", img_url)
        elif isinstance(url, str) and url.startswith("http"):
            self._download_single_image(images_dir, name, url)
    
    def _download_single_image(self, images_dir: Path, name: str, url: str):
        """Download a single image file"""
        try:
            import requests
            response = requests.get(url)
            if response.status_code == 200:
                # Determine extension
                ext = "jpg"
                if "png" in url:
                    ext = "png"
                elif "svg" in url:
                    ext = "svg"
                
                image_path = images_dir / f"{name}.{ext}"
                with open(image_path, 'wb') as f:
                    f.write(response.content)
        except Exception as e:
            logger.error(f"Failed to download image {name}: {e}")
    
    def get_website(self, business_id: str) -> Optional[Dict]:
        """Retrieve a saved website"""
        website_dir = self.base_path / business_id
        
        if not website_dir.exists():
            return None
        
        result = {
            "business_id": business_id,
            "files": {}
        }
        
        # Read HTML
        html_path = website_dir / "index.html"
        if html_path.exists():
            with open(html_path, 'r', encoding='utf-8') as f:
                result["files"]["html"] = f.read()
        
        # Read CSS
        css_path = website_dir / "styles.css"
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                result["files"]["css"] = f.read()
        
        # Read JS
        js_path = website_dir / "script.js"
        if js_path.exists():
            with open(js_path, 'r', encoding='utf-8') as f:
                result["files"]["js"] = f.read()
        
        # Read metadata
        metadata_path = website_dir / "metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                result["metadata"] = json.load(f)
        
        return result
    
    def create_zip_bundle(self, business_id: str) -> Optional[str]:
        """Create a downloadable ZIP file of the website"""
        website_dir = self.base_path / business_id
        
        if not website_dir.exists():
            return None
        
        # Create zip file
        zip_path = self.base_path / f"{business_id}.zip"
        shutil.make_archive(
            str(zip_path.with_suffix('')),
            'zip',
            website_dir
        )
        
        return str(zip_path)
    
    def list_websites(self) -> list:
        """List all stored websites"""
        websites = []
        
        for item in self.base_path.iterdir():
            if item.is_dir() and item.name != "templates":
                metadata_path = item / "metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        websites.append({
                            "business_id": item.name,
                            "generated_at": metadata.get("generated_at"),
                            "preview_url": f"/preview/{item.name}"
                        })
        
        return sorted(websites, key=lambda x: x["generated_at"], reverse=True)
    
    def delete_website(self, business_id: str) -> bool:
        """Delete a stored website"""
        website_dir = self.base_path / business_id
        
        if website_dir.exists():
            shutil.rmtree(website_dir)
            
            # Remove static symlink
            static_link = self.static_path / business_id
            if static_link.exists():
                static_link.unlink()
            
            return True
        
        return False


class WebsiteVersioning:
    """Handle versioning of generated websites"""
    
    def __init__(self, storage: WebsiteStorage):
        self.storage = storage
        self.versions_dir = storage.base_path / "versions"
        self.versions_dir.mkdir(exist_ok=True)
    
    def save_version(self, business_id: str, version_name: str = None):
        """Save a version of the current website"""
        
        if not version_name:
            version_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        source = self.storage.base_path / business_id
        dest = self.versions_dir / business_id / version_name
        dest.parent.mkdir(exist_ok=True)
        
        if source.exists():
            shutil.copytree(source, dest)
            return version_name
        
        return None
    
    def restore_version(self, business_id: str, version_name: str):
        """Restore a specific version"""
        
        version_path = self.versions_dir / business_id / version_name
        current_path = self.storage.base_path / business_id
        
        if version_path.exists():
            # Backup current version
            self.save_version(business_id, "backup_before_restore")
            
            # Remove current
            if current_path.exists():
                shutil.rmtree(current_path)
            
            # Copy version to current
            shutil.copytree(version_path, current_path)
            return True
        
        return False
    
    def list_versions(self, business_id: str) -> list:
        """List all versions for a business"""
        
        versions_path = self.versions_dir / business_id
        if not versions_path.exists():
            return []
        
        versions = []
        for version_dir in versions_path.iterdir():
            if version_dir.is_dir():
                metadata_path = version_dir / "metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        versions.append({
                            "name": version_dir.name,
                            "generated_at": metadata.get("generated_at")
                        })
        
        return sorted(versions, key=lambda x: x["name"], reverse=True)