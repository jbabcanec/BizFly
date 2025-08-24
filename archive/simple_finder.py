#!/usr/bin/env python3

import json
import urllib.request
import urllib.parse
from enum import Enum

class WebsiteType(Enum):
    NO_WEBSITE = "NO_WEBSITE"
    FACEBOOK_ONLY = "FACEBOOK_ONLY" 
    HAS_TRADITIONAL = "HAS_TRADITIONAL"

def classify_website(website_uri):
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

def geocode_location(location, api_key):
    """Geocode a location using Google Geocoding API."""
    encoded_location = urllib.parse.quote(location)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded_location}&key={api_key}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        if data['status'] == 'OK' and data['results']:
            location_data = data['results'][0]['geometry']['location']
            return location_data['lat'], location_data['lng']
        else:
            raise Exception(f"Geocoding failed: {data.get('status', 'Unknown error')}")
    except Exception as e:
        raise Exception(f"Geocoding error: {e}")

def search_nearby_places(lat, lng, radius_miles, api_key):
    """Search for nearby places using Google Places API."""
    radius_meters = int(radius_miles * 1609.34)
    
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius_meters}&key={api_key}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        if data['status'] == 'OK':
            return data.get('results', [])
        else:
            raise Exception(f"Places search failed: {data.get('status', 'Unknown error')}")
    except Exception as e:
        raise Exception(f"Places API error: {e}")

def get_place_details(place_id, api_key):
    """Get detailed information about a place."""
    fields = "name,formatted_address,website,geometry,url"
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={api_key}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        if data['status'] == 'OK':
            return data['result']
        else:
            return None
    except Exception as e:
        print(f"Error getting details for place {place_id}: {e}")
        return None

def find_businesses_pittsburgh(api_key):
    """Find businesses in Pittsburgh, PA and classify their websites."""
    
    print("🔍 BUSINESS FINDER - Pittsburgh, PA")
    print("=" * 60)
    
    try:
        # Geocode Pittsburgh, PA
        print("📍 Geocoding Pittsburgh, PA...")
        lat, lng = geocode_location("Pittsburgh, PA", api_key)
        print(f"   Coordinates: {lat}, {lng}")
        
        # Search for nearby places
        print("🔎 Searching for businesses within 2 miles...")
        places = search_nearby_places(lat, lng, 2.0, api_key)
        print(f"   Found {len(places)} places")
        
        # Get details for each place
        businesses = []
        counts = {
            WebsiteType.NO_WEBSITE: 0,
            WebsiteType.FACEBOOK_ONLY: 0,
            WebsiteType.HAS_TRADITIONAL: 0
        }
        
        print("📋 Getting business details...")
        for i, place in enumerate(places[:20]):  # Limit to first 20 to avoid quota issues
            print(f"   Processing {i+1}/{min(20, len(places))}: {place.get('name', 'Unknown')}")
            
            details = get_place_details(place['place_id'], api_key)
            if details:
                website_type = classify_website(details.get('website'))
                counts[website_type] += 1
                
                business = {
                    'name': details.get('name', 'Unknown'),
                    'address': details.get('formatted_address', 'Unknown'),
                    'website': details.get('website'),
                    'website_type': website_type,
                    'lat': details['geometry']['location']['lat'],
                    'lng': details['geometry']['location']['lng'],
                    'google_maps_url': details.get('url', '')
                }
                businesses.append(business)
        
        # Display results
        total = len(businesses)
        print(f"\n📊 SUMMARY:")
        print(f"Total businesses analyzed: {total}")
        print(f"No website: {counts[WebsiteType.NO_WEBSITE]}")
        print(f"Facebook/Google Sites only: {counts[WebsiteType.FACEBOOK_ONLY]}")
        print(f"Traditional website: {counts[WebsiteType.HAS_TRADITIONAL]}")
        
        # Show businesses without traditional websites
        no_traditional = [b for b in businesses if b['website_type'] in [WebsiteType.NO_WEBSITE, WebsiteType.FACEBOOK_ONLY]]
        
        print(f"\n🎯 BUSINESSES WITHOUT TRADITIONAL WEBSITES ({len(no_traditional)}):")
        print("-" * 80)
        
        for business in no_traditional:
            print(f"• {business['name']}")
            print(f"  Address: {business['address']}")
            print(f"  Type: {business['website_type'].value}")
            if business['website']:
                print(f"  Website: {business['website']}")
            print(f"  Google Maps: {business['google_maps_url']}")
            print()
        
        # Show all businesses in table format
        print(f"\n📋 ALL BUSINESSES:")
        print("-" * 100)
        print(f"{'Name':<25} {'Type':<15} {'Website':<40}")
        print("-" * 100)
        
        for business in businesses:
            name = business['name'][:24]
            website_type = business['website_type'].value
            website = business['website'][:39] if business['website'] else 'None'
            print(f"{name:<25} {website_type:<15} {website:<40}")
        
        # Generate CSV
        print(f"\n💾 CSV FORMAT:")
        print("Name,Address,Latitude,Longitude,Website,Website_Type,Google_Maps_URL")
        for business in businesses:
            website = business['website'] or ''
            print(f'"{business["name"]}","{business["address"]}",{business["lat"]},{business["lng"]},"{website}",{business["website_type"].value},"{business["google_maps_url"]}"')
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    api_key = "AIzaSyBG_awdjVL64U5RoSt3WwX__a6BnCkBfgE"
    find_businesses_pittsburgh(api_key)