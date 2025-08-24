#!/usr/bin/env python3

import os
import sys
import click
from business_finder import BusinessFinder, WebsiteType


@click.command()
@click.option('--location', '-l', required=True, 
              help='Location (address, city, or lat,lng coordinates)')
@click.option('--radius', '-r', default=5.0, 
              help='Search radius in miles (default: 5)')
@click.option('--types', '-t', 
              help='Business types (comma-separated: restaurant,cafe,store,etc)')
@click.option('--filter', '-f', 
              type=click.Choice(['no-website', 'facebook-only', 'traditional'], case_sensitive=False),
              help='Filter by website type')
@click.option('--output', '-o', 
              help='Output CSV filename (optional)')
@click.option('--api-key', 
              envvar='GOOGLE_MAPS_API_KEY',
              help='Google Maps API key (or set GOOGLE_MAPS_API_KEY env var)')
def find_businesses(location, radius, types, filter, output, api_key):
    """Find businesses near a location and analyze their website presence.
    
    Example usage:
    python cli.py -l "New York, NY" -r 2 -f facebook-only
    python cli.py -l "40.7128,-74.0060" -r 1 -t restaurant,cafe
    """
    
    if not api_key:
        click.echo("Error: Google Maps API key required. Set GOOGLE_MAPS_API_KEY environment variable or use --api-key")
        sys.exit(1)
    
    try:
        finder = BusinessFinder(api_key)
        
        # Parse business types
        business_types = None
        if types:
            business_types = [t.strip() for t in types.split(',')]
        
        click.echo(f"Searching for businesses near '{location}' within {radius} miles...")
        
        # Find businesses
        businesses = finder.find_businesses(location, radius, business_types)
        
        if not businesses:
            click.echo("No businesses found.")
            return
        
        # Apply filter if specified
        if filter:
            filter_map = {
                'no-website': [WebsiteType.NO_WEBSITE],
                'facebook-only': [WebsiteType.FACEBOOK_ONLY],
                'traditional': [WebsiteType.HAS_TRADITIONAL]
            }
            businesses = finder.filter_by_website_type(businesses, filter_map[filter])
        
        # Generate report
        report = finder.generate_report(businesses)
        
        # Display summary
        click.echo(f"\n📊 SUMMARY:")
        click.echo(f"Total businesses found: {report['total_businesses']}")
        click.echo(f"No website: {report['no_website']}")
        click.echo(f"Facebook/Google Sites only: {report['facebook_only']}")
        click.echo(f"Traditional website: {report['has_traditional']}")
        
        # Display table
        click.echo(f"\n📋 BUSINESS DETAILS:")
        finder.display_table(businesses)
        
        # Export to CSV if requested
        if output:
            finder.export_to_csv(businesses, output)
            click.echo(f"\n💾 Results exported to {output}")
        
        # Show example businesses with no traditional website
        no_website_businesses = finder.filter_by_website_type(
            businesses, [WebsiteType.NO_WEBSITE, WebsiteType.FACEBOOK_ONLY]
        )
        
        if no_website_businesses and not filter:
            click.echo(f"\n🎯 BUSINESSES WITHOUT TRADITIONAL WEBSITES:")
            finder.display_table(no_website_businesses[:10])  # Show first 10
        
    except Exception as e:
        click.echo(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    find_businesses()