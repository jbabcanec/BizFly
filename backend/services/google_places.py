import googlemaps
from typing import List, Optional, Dict, Any
import logging

from core.config import settings
from models.business import WebsiteStatus

logger = logging.getLogger(__name__)


class GooglePlacesService:
    def __init__(self):
        self.client = googlemaps.Client(key=settings.google_maps_api_key)
    
    async def search_businesses(
        self,
        location: str,
        radius_miles: float,
        business_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        try:
            if ',' in location and location.replace(',', '').replace('.', '').replace('-', '').replace(' ', '').isdigit():
                lat, lng = map(float, location.split(','))
                location_coords = (lat, lng)
            else:
                geocode_result = self.client.geocode(location)
                if not geocode_result:
                    raise ValueError(f"Could not geocode location: {location}")
                location_coords = (
                    geocode_result[0]['geometry']['location']['lat'],
                    geocode_result[0]['geometry']['location']['lng']
                )
            
            radius_meters = int(radius_miles * 1609.34)
            
            search_params = {
                'location': location_coords,
                'radius': radius_meters,
            }
            
            if business_types and business_types[0]:
                search_params['type'] = business_types[0]
            
            places_result = self.client.places_nearby(**search_params)
            
            businesses = []
            for place in places_result.get('results', []):
                place_id = place['place_id']
                
                try:
                    details = self.client.place(
                        place_id=place_id,
                        fields=['website', 'name', 'formatted_address', 
                               'geometry/location', 'url', 'formatted_phone_number',
                               'types']
                    )['result']
                    
                    website = details.get('website')
                    website_status = self._classify_website(website)
                    
                    business_data = {
                        'place_id': place_id,
                        'name': details.get('name', 'Unknown'),
                        'address': details.get('formatted_address', 'Unknown'),
                        'latitude': details['geometry']['location']['lat'],
                        'longitude': details['geometry']['location']['lng'],
                        'phone': details.get('formatted_phone_number'),
                        'website': website,
                        'website_status': website_status,
                        'google_maps_url': details.get('url'),
                        'business_type': details.get('types', [None])[0]
                    }
                    
                    businesses.append(business_data)
                    
                except Exception as e:
                    logger.error(f"Failed to get details for place {place_id}: {e}")
                    continue
            
            return businesses
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
    
    def _classify_website(self, website: Optional[str]) -> WebsiteStatus:
        if not website:
            return WebsiteStatus.NO_WEBSITE
        
        website_lower = website.lower()
        
        facebook_domains = ['facebook.com', 'm.facebook.com']
        for domain in facebook_domains:
            if domain in website_lower:
                return WebsiteStatus.FACEBOOK_ONLY
        
        if website_lower.endswith('.business.site'):
            return WebsiteStatus.FACEBOOK_ONLY
        
        return WebsiteStatus.HAS_WEBSITE