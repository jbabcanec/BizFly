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

def search_restaurants_pittsburgh(api_key):
    """Search specifically for restaurants in Pittsburgh neighborhoods."""
    
    print("🍕 RESTAURANT FINDER - Pittsburgh, PA")
    print("=" * 60)
    
    # Focus on neighborhoods known for local restaurants
    neighborhoods = [
        ("Lawrenceville", 40.4653, -79.9608),
        ("Shadyside", 40.4511, -79.9425),
        ("South Side", 40.4297, -79.9756),
        ("Strip District", 40.4515, -79.9609)
    ]
    
    all_businesses = []
    counts = {
        WebsiteType.NO_WEBSITE: 0,
        WebsiteType.FACEBOOK_ONLY: 0,
        WebsiteType.HAS_TRADITIONAL: 0
    }
    
    for neighborhood, lat, lng in neighborhoods:
        print(f"\n🔎 Searching in {neighborhood}...")
        
        # Search for restaurants specifically
        radius_meters = 805  # 0.5 miles
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius_meters}&type=restaurant&key={api_key}"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
            if data['status'] == 'OK':
                places = data.get('results', [])
                print(f"   Found {len(places)} restaurants")
                
                # Get details for first 8 restaurants in each neighborhood
                for i, place in enumerate(places[:8]):
                    print(f"   Processing: {place.get('name', 'Unknown')}")
                    
                    # Get place details
                    place_id = place['place_id']
                    fields = "name,formatted_address,website,geometry,url,price_level,rating"
                    detail_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={api_key}"
                    
                    try:
                        with urllib.request.urlopen(detail_url) as detail_response:
                            detail_data = json.loads(detail_response.read().decode())
                            
                        if detail_data['status'] == 'OK':
                            details = detail_data['result']
                            website_type = classify_website(details.get('website'))
                            counts[website_type] += 1
                            
                            business = {
                                'name': details.get('name', 'Unknown'),
                                'address': details.get('formatted_address', 'Unknown'),
                                'neighborhood': neighborhood,
                                'website': details.get('website'),
                                'website_type': website_type,
                                'rating': details.get('rating'),
                                'price_level': details.get('price_level'),
                                'lat': details['geometry']['location']['lat'],
                                'lng': details['geometry']['location']['lng'],
                                'google_maps_url': details.get('url', '')
                            }
                            all_businesses.append(business)
                    except Exception as e:
                        print(f"     Error getting details: {e}")
                        continue
                        
            else:
                print(f"   Search failed: {data.get('status', 'Unknown error')}")
                
        except Exception as e:
            print(f"   Error searching {neighborhood}: {e}")
    
    # Display results
    total = len(all_businesses)
    print(f"\n📊 SUMMARY:")
    print(f"Total restaurants analyzed: {total}")
    print(f"No website: {counts[WebsiteType.NO_WEBSITE]}")
    print(f"Facebook/Google Sites only: {counts[WebsiteType.FACEBOOK_ONLY]}")
    print(f"Traditional website: {counts[WebsiteType.HAS_TRADITIONAL]}")
    
    # Show businesses without traditional websites
    no_traditional = [b for b in all_businesses if b['website_type'] in [WebsiteType.NO_WEBSITE, WebsiteType.FACEBOOK_ONLY]]
    
    print(f"\n🎯 RESTAURANTS WITHOUT TRADITIONAL WEBSITES ({len(no_traditional)}):")
    print("-" * 90)
    
    for business in no_traditional:
        print(f"• {business['name']} ({business['neighborhood']})")
        print(f"  Address: {business['address']}")
        print(f"  Type: {business['website_type'].value}")
        if business['website']:
            print(f"  Website: {business['website']}")
        if business['rating']:
            print(f"  Rating: {business['rating']}/5")
        print(f"  Google Maps: {business['google_maps_url']}")
        print()
    
    # Show summary by neighborhood
    print(f"\n📍 BY NEIGHBORHOOD:")
    for neighborhood in ["Lawrenceville", "Shadyside", "South Side", "Strip District"]:
        neighborhood_businesses = [b for b in all_businesses if b['neighborhood'] == neighborhood]
        no_website_count = len([b for b in neighborhood_businesses if b['website_type'] in [WebsiteType.NO_WEBSITE, WebsiteType.FACEBOOK_ONLY]])
        print(f"{neighborhood}: {len(neighborhood_businesses)} restaurants, {no_website_count} without traditional websites")
    
    return all_businesses

if __name__ == "__main__":
    api_key = "AIzaSyBG_awdjVL64U5RoSt3WwX__a6BnCkBfgE"
    businesses = search_restaurants_pittsburgh(api_key)