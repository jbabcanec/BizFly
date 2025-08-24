import re
import csv
import json
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import pandas as pd
import googlemaps
from geopy.geocoders import Nominatim
from tabulate import tabulate


class WebsiteType(Enum):
    NO_WEBSITE = "NO_WEBSITE"
    FACEBOOK_ONLY = "FACEBOOK_ONLY" 
    HAS_TRADITIONAL = "HAS_TRADITIONAL"


@dataclass
class Business:
    name: str
    address: str
    latitude: float
    longitude: float
    website: Optional[str]
    website_type: WebsiteType
    google_maps_url: str
    place_id: str


class BusinessFinder:
    def __init__(self, google_maps_api_key: str):
        self.gmaps = googlemaps.Client(key=google_maps_api_key)
        self.geocoder = Nominatim(user_agent="business_finder")
    
    def _parse_location(self, location_input: str) -> Tuple[float, float]:
        """Parse location input and return lat, lng coordinates."""
        # Check if input looks like coordinates (lat,lng)
        coord_pattern = r'^(-?\d+\.?\d*),\s*(-?\d+\.?\d*)$'
        match = re.match(coord_pattern, location_input.strip())
        
        if match:
            lat, lng = float(match.group(1)), float(match.group(2))
            return lat, lng
        
        # Otherwise, geocode the address/city
        try:
            location = self.geocoder.geocode(location_input)
            if location:
                return location.latitude, location.longitude
            else:
                raise ValueError(f"Could not geocode location: {location_input}")
        except Exception as e:
            raise ValueError(f"Geocoding failed: {e}")
    
    def _classify_website(self, website_uri: Optional[str]) -> WebsiteType:
        """Classify website type based on URL."""
        if not website_uri:
            return WebsiteType.NO_WEBSITE
        
        website_lower = website_uri.lower()
        
        # Check for Facebook pages
        facebook_domains = ['facebook.com', 'm.facebook.com']
        for domain in facebook_domains:
            if domain in website_lower:
                return WebsiteType.FACEBOOK_ONLY
        
        # Check for Google business sites
        if website_lower.endswith('.business.site'):
            return WebsiteType.FACEBOOK_ONLY
        
        return WebsiteType.HAS_TRADITIONAL
    
    def find_businesses(
        self, 
        location: str, 
        radius_miles: float,
        business_types: Optional[List[str]] = None
    ) -> List[Business]:
        """Find businesses near a location and classify their websites."""
        
        # Parse location
        lat, lng = self._parse_location(location)
        
        # Convert miles to meters
        radius_meters = int(radius_miles * 1609.34)
        
        # Search for places
        search_params = {
            'location': (lat, lng),
            'radius': radius_meters,
        }
        
        if business_types:
            search_params['type'] = business_types[0]  # Primary type
        
        try:
            places_result = self.gmaps.places_nearby(**search_params)
        except Exception as e:
            raise ValueError(f"Places API search failed: {e}")
        
        businesses = []
        
        for place in places_result.get('results', []):
            place_id = place['place_id']
            
            # Get detailed information
            try:
                details = self.gmaps.place(
                    place_id=place_id,
                    fields=['website', 'name', 'formatted_address', 
                           'geometry/location', 'url']
                )['result']
                
                business = Business(
                    name=details.get('name', 'Unknown'),
                    address=details.get('formatted_address', 'Unknown'),
                    latitude=details['geometry']['location']['lat'],
                    longitude=details['geometry']['location']['lng'],
                    website=details.get('website'),
                    website_type=self._classify_website(details.get('website')),
                    google_maps_url=details.get('url', ''),
                    place_id=place_id
                )
                
                businesses.append(business)
                
            except Exception as e:
                print(f"Failed to get details for place {place_id}: {e}")
                continue
        
        return businesses
    
    def filter_by_website_type(
        self, 
        businesses: List[Business], 
        website_types: List[WebsiteType]
    ) -> List[Business]:
        """Filter businesses by website type."""
        return [b for b in businesses if b.website_type in website_types]
    
    def generate_report(self, businesses: List[Business]) -> Dict:
        """Generate a summary report of businesses."""
        total = len(businesses)
        
        counts = {
            WebsiteType.NO_WEBSITE: 0,
            WebsiteType.FACEBOOK_ONLY: 0,
            WebsiteType.HAS_TRADITIONAL: 0
        }
        
        for business in businesses:
            counts[business.website_type] += 1
        
        return {
            'total_businesses': total,
            'no_website': counts[WebsiteType.NO_WEBSITE],
            'facebook_only': counts[WebsiteType.FACEBOOK_ONLY],
            'has_traditional': counts[WebsiteType.HAS_TRADITIONAL],
            'businesses': businesses
        }
    
    def export_to_csv(self, businesses: List[Business], filename: str):
        """Export businesses to CSV file."""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'Name', 'Address', 'Latitude', 'Longitude', 
                'Website', 'Website_Type', 'Google_Maps_URL'
            ])
            
            for business in businesses:
                writer.writerow([
                    business.name,
                    business.address,
                    business.latitude,
                    business.longitude,
                    business.website or '',
                    business.website_type.value,
                    business.google_maps_url
                ])
    
    def display_table(self, businesses: List[Business]):
        """Display businesses in a formatted table."""
        if not businesses:
            print("No businesses found.")
            return
        
        table_data = []
        for business in businesses:
            table_data.append([
                business.name[:30] + '...' if len(business.name) > 30 else business.name,
                business.address[:40] + '...' if len(business.address) > 40 else business.address,
                business.website_type.value,
                business.website[:50] + '...' if business.website and len(business.website) > 50 else (business.website or 'None')
            ])
        
        headers = ['Name', 'Address', 'Website Type', 'Website']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))