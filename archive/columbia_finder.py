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

def search_columbia_businesses(api_key):
    """Search for various business types in Columbia, SC."""
    
    print("🔍 BUSINESS FINDER - Columbia, SC")
    print("=" * 60)
    
    # Columbia SC areas and business types to search
    search_areas = [
        ("Downtown Columbia", 34.0007, -81.0348, ["restaurant", "cafe", "store"]),
        ("Five Points", 34.0037, -81.0292, ["restaurant", "bar", "store"]),
        ("The Vista", 34.0010, -81.0403, ["restaurant", "art_gallery", "store"]), 
        ("Forest Drive", 34.0421, -80.9626, ["restaurant", "beauty_salon", "store"]),
        ("Devine Street", 34.0198, -80.9943, ["restaurant", "clothing_store", "store"])
    ]
    
    all_businesses = []
    counts = {
        WebsiteType.NO_WEBSITE: 0,
        WebsiteType.FACEBOOK_ONLY: 0,
        WebsiteType.HAS_TRADITIONAL: 0
    }
    
    for area_name, lat, lng, business_types in search_areas:
        print(f"\n🔎 Searching in {area_name}...")
        
        for business_type in business_types:
            print(f"   Looking for {business_type}s...")
            
            # Search for specific business type
            radius_meters = 1000  # ~0.6 miles
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius_meters}&type={business_type}&key={api_key}"
            
            try:
                with urllib.request.urlopen(url) as response:
                    data = json.loads(response.read().decode())
                    
                if data['status'] == 'OK':
                    places = data.get('results', [])
                    print(f"     Found {len(places)} {business_type}s")
                    
                    # Get details for first 4 businesses of each type in each area
                    for i, place in enumerate(places[:4]):
                        business_name = place.get('name', 'Unknown')
                        print(f"     Processing: {business_name}")
                        
                        # Get place details
                        place_id = place['place_id']
                        fields = "name,formatted_address,website,geometry,url,price_level,rating,types"
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
                                    'area': area_name,
                                    'business_type': business_type,
                                    'website': details.get('website'),
                                    'website_type': website_type,
                                    'rating': details.get('rating'),
                                    'price_level': details.get('price_level'),
                                    'types': details.get('types', []),
                                    'lat': details['geometry']['location']['lat'],
                                    'lng': details['geometry']['location']['lng'],
                                    'google_maps_url': details.get('url', '')
                                }
                                all_businesses.append(business)
                        except Exception as e:
                            print(f"       Error getting details: {e}")
                            continue
                            
                else:
                    print(f"     Search failed: {data.get('status', 'Unknown error')}")
                    
            except Exception as e:
                print(f"     Error searching {business_type}s in {area_name}: {e}")
    
    # Remove duplicates based on name and address
    unique_businesses = []
    seen = set()
    for business in all_businesses:
        key = (business['name'], business['address'])
        if key not in seen:
            seen.add(key)
            unique_businesses.append(business)
    
    # Recalculate counts for unique businesses
    counts = {
        WebsiteType.NO_WEBSITE: 0,
        WebsiteType.FACEBOOK_ONLY: 0,
        WebsiteType.HAS_TRADITIONAL: 0
    }
    for business in unique_businesses:
        counts[business['website_type']] += 1
    
    # Display results
    total = len(unique_businesses)
    print(f"\n📊 SUMMARY:")
    print(f"Total unique businesses analyzed: {total}")
    print(f"No website: {counts[WebsiteType.NO_WEBSITE]} ({counts[WebsiteType.NO_WEBSITE]/total*100:.1f}%)")
    print(f"Facebook/Google Sites only: {counts[WebsiteType.FACEBOOK_ONLY]} ({counts[WebsiteType.FACEBOOK_ONLY]/total*100:.1f}%)")
    print(f"Traditional website: {counts[WebsiteType.HAS_TRADITIONAL]} ({counts[WebsiteType.HAS_TRADITIONAL]/total*100:.1f}%)")
    
    # Show businesses without traditional websites
    no_traditional = [b for b in unique_businesses if b['website_type'] in [WebsiteType.NO_WEBSITE, WebsiteType.FACEBOOK_ONLY]]
    
    print(f"\n🎯 BUSINESSES WITHOUT TRADITIONAL WEBSITES ({len(no_traditional)}):")
    print("-" * 100)
    
    for business in no_traditional:
        print(f"• {business['name']} ({business['area']})")
        print(f"  Type: {business['business_type'].replace('_', ' ').title()} | {business['website_type'].value}")
        print(f"  Address: {business['address']}")
        if business['website']:
            print(f"  Website: {business['website']}")
        if business['rating']:
            print(f"  Rating: {business['rating']}/5 ⭐")
        print(f"  Google Maps: {business['google_maps_url']}")
        print()
    
    # Show summary by area
    print(f"\n📍 BY AREA:")
    for area in ["Downtown Columbia", "Five Points", "The Vista", "Forest Drive", "Devine Street"]:
        area_businesses = [b for b in unique_businesses if b['area'] == area]
        no_website_count = len([b for b in area_businesses if b['website_type'] in [WebsiteType.NO_WEBSITE, WebsiteType.FACEBOOK_ONLY]])
        if area_businesses:
            print(f"{area}: {len(area_businesses)} businesses, {no_website_count} without traditional websites")
    
    # Show summary by business type
    print(f"\n🏪 BY BUSINESS TYPE:")
    business_type_summary = {}
    for business in unique_businesses:
        btype = business['business_type']
        if btype not in business_type_summary:
            business_type_summary[btype] = {'total': 0, 'no_website': 0}
        business_type_summary[btype]['total'] += 1
        if business['website_type'] in [WebsiteType.NO_WEBSITE, WebsiteType.FACEBOOK_ONLY]:
            business_type_summary[btype]['no_website'] += 1
    
    for btype, stats in business_type_summary.items():
        percentage = stats['no_website']/stats['total']*100 if stats['total'] > 0 else 0
        print(f"{btype.replace('_', ' ').title()}: {stats['total']} total, {stats['no_website']} without websites ({percentage:.1f}%)")
    
    return unique_businesses

if __name__ == "__main__":
    api_key = "AIzaSyBG_awdjVL64U5RoSt3WwX__a6BnCkBfgE"
    businesses = search_columbia_businesses(api_key)