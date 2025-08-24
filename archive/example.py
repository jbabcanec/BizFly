#!/usr/bin/env python3

import os
from business_finder import BusinessFinder, WebsiteType

def main():
    # Example usage of the BusinessFinder class
    
    # You'll need to set your Google Maps API key
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print("Please set GOOGLE_MAPS_API_KEY environment variable")
        return
    
    finder = BusinessFinder(api_key)
    
    # Example 1: Find restaurants in San Francisco
    print("Example 1: Finding restaurants in San Francisco...")
    try:
        businesses = finder.find_businesses(
            location="San Francisco, CA",
            radius_miles=1.0,
            business_types=["restaurant"]
        )
        
        report = finder.generate_report(businesses)
        print(f"Found {report['total_businesses']} restaurants")
        print(f"- No website: {report['no_website']}")
        print(f"- Facebook only: {report['facebook_only']}")
        print(f"- Traditional website: {report['has_traditional']}")
        
        # Show businesses without traditional websites
        no_traditional = finder.filter_by_website_type(
            businesses, 
            [WebsiteType.NO_WEBSITE, WebsiteType.FACEBOOK_ONLY]
        )
        
        print(f"\nBusinesses without traditional websites ({len(no_traditional)}):")
        for business in no_traditional[:5]:  # Show first 5
            print(f"- {business.name}: {business.website_type.value}")
            if business.website:
                print(f"  Website: {business.website}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Using coordinates
    print("\n" + "="*50)
    print("Example 2: Using coordinates (Times Square, NYC)...")
    try:
        businesses = finder.find_businesses(
            location="40.7580,-73.9855",  # Times Square coordinates
            radius_miles=0.5
        )
        
        # Export to CSV
        finder.export_to_csv(businesses, "times_square_businesses.csv")
        print(f"Exported {len(businesses)} businesses to times_square_businesses.csv")
        
        # Display table
        finder.display_table(businesses[:10])  # Show first 10
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()