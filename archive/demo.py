#!/usr/bin/env python3

# Demo version without external dependencies to show the concept
import json
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

def demo_pittsburgh_businesses():
    """Demo with sample Pittsburgh business data"""
    
    print("🔍 BUSINESS FINDER DEMO - Pittsburgh, PA")
    print("=" * 60)
    
    # Sample business data (what would come from Google Maps API)
    sample_businesses = [
        {
            "name": "Primanti Bros. Restaurant",
            "address": "46 18th St, Pittsburgh, PA 15222",
            "website": "https://primantibros.com",
            "lat": 40.4406, "lng": -79.9959
        },
        {
            "name": "Joe's Corner Store", 
            "address": "123 Carson St, Pittsburgh, PA 15203",
            "website": None,
            "lat": 40.4297, "lng": -79.9756
        },
        {
            "name": "Steel City Coffee",
            "address": "456 Liberty Ave, Pittsburgh, PA 15222", 
            "website": "https://facebook.com/steelcitycoffee",
            "lat": 40.4418, "lng": -79.9901
        },
        {
            "name": "Roberto's Pizzeria",
            "address": "789 Penn Ave, Pittsburgh, PA 15222",
            "website": None,
            "lat": 40.4515, "lng": -79.9755
        },
        {
            "name": "Three Rivers Bakery",
            "address": "321 Market St, Pittsburgh, PA 15222",
            "website": "https://threerivers.business.site",
            "lat": 40.4431, "lng": -79.9944
        },
        {
            "name": "Pittsburgh Brewing Co",
            "address": "654 Smallman St, Pittsburgh, PA 15222", 
            "website": "https://pittsburghbrewing.com",
            "lat": 40.4515, "lng": -79.9609
        },
        {
            "name": "Mom's Diner",
            "address": "987 Butler St, Pittsburgh, PA 15201",
            "website": "https://m.facebook.com/momsdiner",
            "lat": 40.4648, "lng": -79.9514
        }
    ]
    
    # Process and classify businesses
    results = []
    counts = {
        WebsiteType.NO_WEBSITE: 0,
        WebsiteType.FACEBOOK_ONLY: 0,
        WebsiteType.HAS_TRADITIONAL: 0
    }
    
    for business in sample_businesses:
        website_type = classify_website(business['website'])
        counts[website_type] += 1
        
        results.append({
            'name': business['name'],
            'address': business['address'],
            'website': business['website'],
            'website_type': website_type,
            'lat': business['lat'],
            'lng': business['lng']
        })
    
    # Display summary
    total = len(results)
    print(f"\n📊 SUMMARY:")
    print(f"Total businesses found: {total}")
    print(f"No website: {counts[WebsiteType.NO_WEBSITE]}")
    print(f"Facebook/Google Sites only: {counts[WebsiteType.FACEBOOK_ONLY]}")
    print(f"Traditional website: {counts[WebsiteType.HAS_TRADITIONAL]}")
    
    # Display detailed results
    print(f"\n📋 BUSINESS DETAILS:")
    print("-" * 80)
    
    for business in results:
        print(f"Name: {business['name']}")
        print(f"Address: {business['address']}")
        print(f"Website Type: {business['website_type'].value}")
        print(f"Website: {business['website'] or 'None'}")
        print(f"Coordinates: {business['lat']}, {business['lng']}")
        print("-" * 80)
    
    # Show businesses without traditional websites
    no_traditional = [b for b in results if b['website_type'] in [WebsiteType.NO_WEBSITE, WebsiteType.FACEBOOK_ONLY]]
    
    print(f"\n🎯 BUSINESSES WITHOUT TRADITIONAL WEBSITES ({len(no_traditional)}):")
    print("-" * 60)
    
    for business in no_traditional:
        print(f"• {business['name']}")
        print(f"  Type: {business['website_type'].value}")
        if business['website']:
            print(f"  Facebook/Social: {business['website']}")
        print()
    
    # Generate CSV output
    print("\n💾 CSV FORMAT:")
    print("Name,Address,Latitude,Longitude,Website,Website_Type")
    for business in results:
        website = business['website'] or ''
        print(f'"{business["name"]}","{business["address"]}",{business["lat"]},{business["lng"]},"{website}",{business["website_type"].value}')

if __name__ == "__main__":
    demo_pittsburgh_businesses()