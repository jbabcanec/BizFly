"""
Image Service - Handles image sourcing from multiple providers
"""
import os
import json
import hashlib
import requests
from typing import List, Dict, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ImageService:
    """Service for sourcing and managing images for businesses"""
    
    def __init__(self):
        self.static_dir = Path("static/images")
        self.static_dir.mkdir(parents=True, exist_ok=True)
        
        # Unsplash API (free tier - 50 requests/hour)
        self.unsplash_access_key = os.getenv("UNSPLASH_ACCESS_KEY", "")
        
        # Pexels API (free - 200 requests/hour)
        self.pexels_api_key = os.getenv("PEXELS_API_KEY", "")
        
        # Cache for API responses
        self.cache_dir = Path("cache/images")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_images_for_business(self, business_type: str, business_name: str) -> Dict[str, str]:
        """
        Get relevant images for a business
        Returns URLs that can be used directly in HTML
        """
        images = {
            "hero": self._get_hero_image(business_type),
            "gallery": self._get_gallery_images(business_type),
            "logo": self._generate_logo_placeholder(business_name),
            "map": self._get_map_placeholder()
        }
        return images
    
    def _get_hero_image(self, business_type: str) -> str:
        """Get a hero image based on business type"""
        
        # Use Unsplash API for high-quality images
        if self.unsplash_access_key:
            try:
                query = self._get_search_query(business_type, "hero")
                url = f"https://api.unsplash.com/search/photos"
                params = {
                    "query": query,
                    "per_page": 1,
                    "orientation": "landscape"
                }
                headers = {"Authorization": f"Client-ID {self.unsplash_access_key}"}
                
                response = requests.get(url, params=params, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    if data["results"]:
                        # Return optimized URL (w=1200 for hero images)
                        return data["results"][0]["urls"]["regular"]
            except Exception as e:
                logger.error(f"Unsplash API error: {e}")
        
        # Fallback to free stock photo services
        return self._get_fallback_image(business_type, "hero")
    
    def _get_gallery_images(self, business_type: str, count: int = 4) -> List[str]:
        """Get gallery images for the business"""
        images = []
        
        # Try Pexels API (completely free)
        if self.pexels_api_key:
            try:
                query = self._get_search_query(business_type, "gallery")
                url = "https://api.pexels.com/v1/search"
                params = {
                    "query": query,
                    "per_page": count,
                    "size": "medium"
                }
                headers = {"Authorization": self.pexels_api_key}
                
                response = requests.get(url, params=params, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    for photo in data["photos"]:
                        images.append(photo["src"]["large"])
            except Exception as e:
                logger.error(f"Pexels API error: {e}")
        
        # If not enough images, use fallbacks
        while len(images) < count:
            images.append(self._get_fallback_image(business_type, f"gallery_{len(images)}"))
        
        return images[:count]
    
    def _get_fallback_image(self, business_type: str, image_type: str) -> str:
        """Get fallback images from free services that don't require API keys"""
        
        # Picsum - Lorem Ipsum for photos (no API key needed)
        seed = hashlib.md5(f"{business_type}_{image_type}".encode()).hexdigest()[:10]
        width = 1200 if image_type == "hero" else 800
        height = 600 if image_type == "hero" else 600
        
        # Returns a consistent image based on seed
        return f"https://picsum.photos/seed/{seed}/{width}/{height}"
    
    def _generate_logo_placeholder(self, business_name: str) -> str:
        """Generate a logo placeholder using UI avatars service"""
        # UI Avatars - free service for generating avatar placeholders
        initials = "".join([word[0].upper() for word in business_name.split()[:2]])
        
        params = {
            "name": initials,
            "size": 200,
            "background": "667eea",
            "color": "ffffff",
            "bold": "true",
            "format": "svg"
        }
        
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://ui-avatars.com/api/?{param_str}"
    
    def _get_map_placeholder(self) -> str:
        """Get a map placeholder image"""
        # Use OpenStreetMap static image
        return "https://via.placeholder.com/800x400/e2e8f0/64748b?text=Map+Location"
    
    def _get_search_query(self, business_type: str, context: str) -> str:
        """Generate smart search queries based on business type"""
        
        # Business type mappings for better image results
        queries = {
            "restaurant": {
                "hero": "restaurant interior elegant dining",
                "gallery": "food plating gourmet cuisine"
            },
            "salon": {
                "hero": "hair salon modern interior",
                "gallery": "hairstyling beauty salon"
            },
            "gym": {
                "hero": "fitness gym equipment modern",
                "gallery": "workout training fitness"
            },
            "coffee": {
                "hero": "coffee shop cozy interior",
                "gallery": "coffee latte barista"
            },
            "retail": {
                "hero": "retail store shopping interior",
                "gallery": "products shopping retail"
            },
            "medical": {
                "hero": "medical office modern clean",
                "gallery": "healthcare medical professional"
            },
            "auto": {
                "hero": "auto repair shop garage",
                "gallery": "car maintenance mechanic"
            }
        }
        
        # Find best match for business type
        for key in queries:
            if key in business_type.lower():
                return queries[key].get(context, queries[key]["hero"])
        
        # Default query
        return f"{business_type} business professional"
    
    def download_and_cache_image(self, url: str, business_id: str, image_type: str) -> str:
        """Download image and cache locally for faster serving"""
        
        # Create business-specific directory
        business_dir = self.static_dir / business_id
        business_dir.mkdir(exist_ok=True)
        
        # Generate filename
        ext = url.split(".")[-1].split("?")[0][:4]  # Get extension, max 4 chars
        if ext not in ["jpg", "jpeg", "png", "webp", "svg"]:
            ext = "jpg"
        
        filename = f"{image_type}.{ext}"
        filepath = business_dir / filename
        
        # Download if not cached
        if not filepath.exists():
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
            except Exception as e:
                logger.error(f"Failed to download image: {e}")
                return url  # Return original URL as fallback
        
        # Return local static URL
        return f"/static/images/{business_id}/{filename}"


class BusinessImageSet:
    """Container for a complete set of business images"""
    
    def __init__(self, business_type: str, business_name: str):
        self.service = ImageService()
        self.images = self.service.get_images_for_business(business_type, business_name)
    
    def get_hero(self) -> str:
        return self.images.get("hero", "")
    
    def get_gallery(self) -> List[str]:
        return self.images.get("gallery", [])
    
    def get_logo(self) -> str:
        return self.images.get("logo", "")
    
    def to_template_data(self) -> Dict:
        """Format for template rendering"""
        return {
            "hero_image": self.get_hero(),
            "logo": self.get_logo(),
            "gallery": self.get_gallery(),
            "has_images": True
        }