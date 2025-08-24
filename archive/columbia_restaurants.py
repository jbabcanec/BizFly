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

def search_columbia_restaurants(api_key):
    """Search specifically for restaurants in Columbia, SC neighborhoods."""
    
    print("🍽️ RESTAURANT FINDER - Columbia, SC")
    print("=" * 60)
    
    # Columbia SC neighborhoods and areas known for local dining
    neighborhoods = [
        ("Five Points", 34.0037, -81.0292),
        ("The Vista", 34.0010, -81.0403),
        ("Forest Drive", 34.0421, -80.9626),
        ("Devine Street", 34.0198, -80.9943),
        ("Rosewood", 34.0332, -81.0129),
        ("North Main Street", 34.0115, -81.0348),
        ("Shandon", 34.0156, -80.9932),
        ("Elmwood Park", 34.0297, -81.0754)
    ]
    
    all_restaurants = []
    counts = {
        WebsiteType.NO_WEBSITE: 0,
        WebsiteType.FACEBOOK_ONLY: 0,
        WebsiteType.HAS_TRADITIONAL: 0
    }
    
    for neighborhood, lat, lng in neighborhoods:
        print(f"\n🔎 Searching restaurants in {neighborhood}...")
        
        # Search for restaurants specifically
        radius_meters = 1200  # ~0.75 miles to get good coverage
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius_meters}&type=restaurant&key={api_key}"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
            if data['status'] == 'OK':
                places = data.get('results', [])
                print(f"   Found {len(places)} restaurants")
                
                # Get details for restaurants, focusing on local/independent ones
                processed = 0
                for place in places:
                    if processed >= 6:  # Limit per neighborhood to avoid quota issues
                        break
                        
                    restaurant_name = place.get('name', 'Unknown')
                    
                    # Skip obvious chains to focus on local restaurants
                    chain_keywords = ['mcdonald', 'subway', 'taco bell', 'kfc', 'pizza hut', 
                                    'domino', 'papa john', 'wendy', 'burger king', 'chick-fil-a',
                                    'chipotle', 'panera', 'starbucks', 'dunkin', 'applebee']
                    
                    if any(keyword in restaurant_name.lower() for keyword in chain_keywords):
                        continue  # Skip chains
                    
                    print(f"   Processing: {restaurant_name}")
                    processed += 1
                    
                    # Get place details
                    place_id = place['place_id']
                    fields = "name,formatted_address,website,geometry,url,price_level,rating,types,opening_hours"
                    detail_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={api_key}"
                    
                    try:
                        with urllib.request.urlopen(detail_url) as detail_response:
                            detail_data = json.loads(detail_response.read().decode())
                            
                        if detail_data['status'] == 'OK':
                            details = detail_data['result']
                            website_type = classify_website(details.get('website'))
                            counts[website_type] += 1
                            
                            restaurant = {
                                'name': details.get('name', 'Unknown'),
                                'address': details.get('formatted_address', 'Unknown'),
                                'neighborhood': neighborhood,
                                'website': details.get('website'),
                                'website_type': website_type,
                                'rating': details.get('rating'),
                                'price_level': details.get('price_level'),
                                'types': details.get('types', []),
                                'lat': details['geometry']['location']['lat'],
                                'lng': details['geometry']['location']['lng'],
                                'google_maps_url': details.get('url', ''),
                                'opening_hours': details.get('opening_hours', {}).get('weekday_text', [])
                            }
                            all_restaurants.append(restaurant)
                    except Exception as e:
                        print(f"     Error getting details: {e}")
                        continue
                        
            elif data['status'] == 'ZERO_RESULTS':
                print(f"   No restaurants found in {neighborhood}")
            else:
                print(f"   Search failed: {data.get('status', 'Unknown error')}")
                
        except Exception as e:
            print(f"   Error searching {neighborhood}: {e}")
    
    # Remove duplicates based on name and address
    unique_restaurants = []
    seen = set()
    for restaurant in all_restaurants:
        key = (restaurant['name'], restaurant['address'])
        if key not in seen:
            seen.add(key)
            unique_restaurants.append(restaurant)
    
    # Recalculate counts for unique restaurants
    counts = {
        WebsiteType.NO_WEBSITE: 0,
        WebsiteType.FACEBOOK_ONLY: 0,
        WebsiteType.HAS_TRADITIONAL: 0
    }
    for restaurant in unique_restaurants:
        counts[restaurant['website_type']] += 1
    
    # Display results
    total = len(unique_restaurants)
    print(f"\n📊 SUMMARY:")
    print(f"Total unique restaurants analyzed: {total}")
    print(f"No website: {counts[WebsiteType.NO_WEBSITE]} ({counts[WebsiteType.NO_WEBSITE]/total*100:.1f}%)")
    print(f"Facebook/Google Sites only: {counts[WebsiteType.FACEBOOK_ONLY]} ({counts[WebsiteType.FACEBOOK_ONLY]/total*100:.1f}%)")
    print(f"Traditional website: {counts[WebsiteType.HAS_TRADITIONAL]} ({counts[WebsiteType.HAS_TRADITIONAL]/total*100:.1f}%)")
    
    # Show restaurants without traditional websites
    no_traditional = [r for r in unique_restaurants if r['website_type'] in [WebsiteType.NO_WEBSITE, WebsiteType.FACEBOOK_ONLY]]
    
    print(f"\n🎯 RESTAURANTS WITHOUT TRADITIONAL WEBSITES ({len(no_traditional)}):")
    print("-" * 100)
    
    for restaurant in no_traditional:
        print(f"• {restaurant['name']} ({restaurant['neighborhood']})")
        print(f"  Address: {restaurant['address']}")
        print(f"  Type: {restaurant['website_type'].value}")
        if restaurant['website']:
            print(f"  Website: {restaurant['website']}")
        if restaurant['rating']:
            print(f"  Rating: {restaurant['rating']}/5 ⭐")
        if restaurant['price_level']:
            price_symbols = '$' * restaurant['price_level']
            print(f"  Price Level: {price_symbols}")
        print(f"  Google Maps: {restaurant['google_maps_url']}")
        print()
    
    # Show all restaurants for reference
    print(f"\n📋 ALL LOCAL RESTAURANTS FOUND:")
    print("-" * 120)
    print(f"{'Name':<30} {'Neighborhood':<15} {'Rating':<8} {'Website Type':<15} {'Website':<40}")
    print("-" * 120)
    
    for restaurant in unique_restaurants:
        name = restaurant['name'][:29]
        neighborhood = restaurant['neighborhood'][:14]
        rating = f"{restaurant['rating']}/5" if restaurant['rating'] else "N/A"
        website_type = restaurant['website_type'].value[:14]
        website = restaurant['website'][:39] if restaurant['website'] else 'None'
        print(f"{name:<30} {neighborhood:<15} {rating:<8} {website_type:<15} {website:<40}")
    
    # Show summary by neighborhood
    print(f"\n📍 BY NEIGHBORHOOD:")
    neighborhood_summary = {}
    for restaurant in unique_restaurants:
        neighborhood = restaurant['neighborhood']
        if neighborhood not in neighborhood_summary:
            neighborhood_summary[neighborhood] = {'total': 0, 'no_website': 0}
        neighborhood_summary[neighborhood]['total'] += 1
        if restaurant['website_type'] in [WebsiteType.NO_WEBSITE, WebsiteType.FACEBOOK_ONLY]:
            neighborhood_summary[neighborhood]['no_website'] += 1
    
    for neighborhood, stats in neighborhood_summary.items():
        percentage = stats['no_website']/stats['total']*100 if stats['total'] > 0 else 0
        print(f"{neighborhood}: {stats['total']} restaurants, {stats['no_website']} without websites ({percentage:.1f}%)")
    
    return unique_restaurants

if __name__ == "__main__":
    api_key = "AIzaSyBG_awdjVL64U5RoSt3WwX__a6BnCkBfgE"
    restaurants = search_columbia_restaurants(api_key)