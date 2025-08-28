import googlemaps
from typing import List, Optional, Dict, Any
import logging
import time

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
        business_types: Optional[List[str]] = None,
        max_results: int = 60  # Maximum results to fetch (3 pages of 20 each)
    ) -> List[Dict[str, Any]]:
        try:
            # Geocode location
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
            
            # Simple approach - get all businesses first, filter after
            all_businesses = []
            seen_place_ids = set()
            
            if business_types and len(business_types) > 0:
                # Search for each business type with chain filtering
                for business_type in business_types:
                    if business_type.strip():
                        type_businesses = await self._search_by_type_smart(
                            location_coords, radius_meters, business_type.strip(), 
                            max_results // len(business_types)
                        )
                        for business in type_businesses:
                            if business['place_id'] not in seen_place_ids:
                                all_businesses.append(business)
                                seen_place_ids.add(business['place_id'])
            else:
                # Smart neighborhood-based search like archive approach
                all_businesses = await self._search_neighborhoods_smart(
                    location, max_results
                )
            
            # Sort by website status FIRST, then popularity - prioritize businesses without websites
            def calculate_popularity_score(business):
                rating = business.get('rating', 0) or 0
                rating_count = business.get('rating_count', 0) or 0
                website_status = business.get('website_status', 'NO_WEBSITE')
                
                # Base popularity score
                base_score = rating * max(1, rating_count)
                
                # MASSIVE boost for businesses without websites (our primary goal)
                if website_status == 'NO_WEBSITE':
                    return 10000 + base_score  # Put NO_WEBSITE businesses first
                elif website_status == 'FACEBOOK_ONLY':  
                    return 5000 + base_score   # Put FACEBOOK_ONLY businesses second
                else:
                    return base_score          # Businesses with websites go last
            
            logger.info("Sorting businesses: NO_WEBSITE first, then FACEBOOK_ONLY, then others")
            
            # Sort by popularity score (highest first)
            all_businesses.sort(key=calculate_popularity_score, reverse=True)
            
            # Limit results
            all_businesses = all_businesses[:max_results]
            
            logger.info(f"Found {len(all_businesses)} businesses, sorted by popularity (prioritizing no website)")
            return all_businesses
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
    
    async def _search_by_type_smart(
        self, 
        location_coords: tuple, 
        radius_meters: int, 
        business_type: str, 
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Search for businesses by specific type with chain filtering"""
        try:
            search_params = {
                'location': location_coords,
                'radius': radius_meters,
                'type': business_type
            }
            
            results = await self._paginated_search(search_params, max_results * 2)  # Get more to filter
            return self._filter_chains(results, max_results)
            
        except Exception as e:
            logger.error(f"Type search failed for '{business_type}': {e}")
            return []
    
    async def _search_neighborhoods_smart(self, location: str, max_results: int) -> List[Dict[str, Any]]:
        """Search specific neighborhoods like archive approach"""
        
        # Define neighborhood coordinates for different cities based on archive data
        city_neighborhoods = {
            'columbia': [
                ("Rosewood", 34.0332, -81.0129),      # 50% no websites in archive
                ("Elmwood Park", 34.0297, -81.0754),   # 80% no websites in archive  
                ("North Main Street", 34.0115, -81.0348),
                ("Devine Street", 34.0198, -80.9943),
                ("The Vista", 34.0010, -81.0403),
                ("Five Points", 34.0037, -81.0292)
            ],
            'pittsburgh': [
                ("Lawrenceville", 40.4653, -79.9608),
                ("Shadyside", 40.4511, -79.9425),
                ("South Side", 40.4297, -79.9756),
                ("Strip District", 40.4515, -79.9609)
            ]
        }
        
        # Determine which city/neighborhoods to use
        location_lower = location.lower()
        neighborhoods = []
        
        if 'columbia' in location_lower or 'sc' in location_lower:
            neighborhoods = city_neighborhoods['columbia']
            logger.info("Using Columbia, SC neighborhoods for targeted search")
        elif 'pittsburgh' in location_lower or 'pennsylvania' in location_lower or 'pa' in location_lower:
            neighborhoods = city_neighborhoods['pittsburgh']
            logger.info("Using Pittsburgh, PA neighborhoods for targeted search")
        else:
            # Fallback to general search around the geocoded location
            logger.info("Unknown location, falling back to general restaurant search")
            geocode_result = self.client.geocode(location)
            if geocode_result:
                location_coords = (
                    geocode_result[0]['geometry']['location']['lat'],
                    geocode_result[0]['geometry']['location']['lng']
                )
                return await self._search_restaurants_smart(location_coords, 5000, max_results)
            return []
        
        # Search each neighborhood with small radius like archive
        all_businesses = []
        seen_place_ids = set()
        businesses_per_neighborhood = max(3, max_results // len(neighborhoods))
        
        for neighborhood, lat, lng in neighborhoods:
            logger.info(f"Searching {neighborhood}...")
            
            # Small radius like archive (1200m = ~0.75 miles)
            search_params = {
                'location': (lat, lng),
                'radius': 1200,  
                'type': 'restaurant'
            }
            
            try:
                # Get restaurants from this neighborhood
                neighborhood_results = await self._paginated_search(search_params, businesses_per_neighborhood * 2)
                
                # Filter chains and add neighborhood info
                filtered_results = self._filter_chains(neighborhood_results, businesses_per_neighborhood)
                
                for business in filtered_results:
                    if business['place_id'] not in seen_place_ids:
                        business['neighborhood'] = neighborhood  # Add neighborhood info
                        all_businesses.append(business)
                        seen_place_ids.add(business['place_id'])
                        
                        # Log target businesses
                        if business['website_status'] in ['NO_WEBSITE', 'FACEBOOK_ONLY']:
                            logger.info(f"  🎯 FOUND TARGET: {business['name']} - {business['website_status']}")
                
                targets_found = len([b for b in filtered_results if b['website_status'] in ['NO_WEBSITE', 'FACEBOOK_ONLY']])
                logger.info(f"  {neighborhood}: {len(filtered_results)} local businesses found, {targets_found} targets")
                
            except Exception as e:
                logger.error(f"Error searching {neighborhood}: {e}")
                continue
        
        logger.info(f"Neighborhood search completed: {len(all_businesses)} total businesses")
        return all_businesses
    
    async def _search_restaurants_smart(
        self, 
        location_coords: tuple, 
        radius_meters: int, 
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Smart restaurant search focusing on local businesses"""
        try:
            search_params = {
                'location': location_coords,
                'radius': radius_meters,
                'type': 'restaurant'  # Specific restaurant search like archive
            }
            
            results = await self._paginated_search(search_params, max_results * 3)  # Get more to filter
            return self._filter_chains(results, max_results)
            
        except Exception as e:
            logger.error(f"Restaurant search failed: {e}")
            return []
    
    async def _search_nearby(
        self, 
        location_coords: tuple, 
        radius_meters: int, 
        max_results: int
    ) -> List[Dict[str, Any]]:
        """General nearby search without type restrictions"""
        try:
            search_params = {
                'location': location_coords,
                'radius': radius_meters
            }
            
            return await self._paginated_search(search_params, max_results)
            
        except Exception as e:
            logger.error(f"Nearby search failed: {e}")
            return []
    
    async def _paginated_search(
        self, 
        search_params: Dict[str, Any], 
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Handle paginated search results"""
        all_businesses = []
        next_page_token = None
        page_count = 0
        max_pages = max(1, max_results // 20)  # Each page returns up to 20 results
        
        while page_count < max_pages and len(all_businesses) < max_results:
            # Add page token if we have one
            if next_page_token:
                search_params['page_token'] = next_page_token
                # Google requires a short delay before using page token
                time.sleep(2)
            
            places_result = self.client.places_nearby(**search_params)
            raw_results = places_result.get('results', [])
            logger.info(f"Page {page_count + 1}: Found {len(raw_results)} raw places from Google API")
            
            # Process current page results - pass types from nearby search
            for place in raw_results:
                if len(all_businesses) >= max_results:
                    break
                    
                # Get types from nearby search result
                place_types = place.get('types', [])
                business_data = await self._get_place_details(place['place_id'], place_types)
                if business_data:  # Only skip if we can't get basic details
                    all_businesses.append(business_data)
            
            # Check if there's a next page
            next_page_token = places_result.get('next_page_token')
            page_count += 1
            
            # If no more pages available, break
            if not next_page_token:
                break
            
            # Remove page_token for next iteration (it gets added above)
            search_params.pop('page_token', None)
        
        logger.info(f"Total collected: {len(all_businesses)} businesses from {page_count} pages")
        return all_businesses
    
    async def _get_place_details(self, place_id: str, place_types: List[str] = None) -> Optional[Dict[str, Any]]:
        """Get detailed information for a specific place"""
        try:
            details = self.client.place(
                place_id=place_id,
                fields=['website', 'name', 'formatted_address', 
                       'geometry/location', 'url', 'formatted_phone_number',
                       'business_status', 'rating', 'user_ratings_total']
            )['result']
            
            # Skip permanently closed businesses
            if details.get('business_status') == 'CLOSED_PERMANENTLY':
                return None
            
            website = details.get('website')
            website_status = self._classify_website(website)
            
            # Use types passed from nearby search (types not available in place details)
            business_types = place_types or []
            
            # Get most specific business type (prioritize restaurant, cafe, etc.)
            business_type = None
            if business_types:
                # Priority order - look for specific business types first
                priority_types = ['restaurant', 'cafe', 'bakery', 'bar', 'meal_takeaway', 'food']
                for ptype in priority_types:
                    if ptype in business_types:
                        business_type = ptype
                        break
                # If no priority type found, use first non-generic type
                if not business_type:
                    generic_types = ['establishment', 'point_of_interest']
                    for btype in business_types:
                        if btype not in generic_types:
                            business_type = btype
                            break
                # Fallback to first type
                if not business_type:
                    business_type = business_types[0]
            
            return {
                'place_id': place_id,
                'name': details.get('name', 'Unknown'),
                'address': details.get('formatted_address', 'Unknown'),
                'latitude': details['geometry']['location']['lat'],
                'longitude': details['geometry']['location']['lng'],
                'phone': details.get('formatted_phone_number'),
                'website': website,
                'website_status': website_status,
                'google_maps_url': details.get('url'),
                'business_type': business_type,
                'rating': details.get('rating'),
                'rating_count': details.get('user_ratings_total')
            }
            
        except Exception as e:
            logger.error(f"Failed to get details for place {place_id}: {e}")
            return None
    
    def _filter_chains(self, businesses: List[Dict[str, Any]], max_results: int) -> List[Dict[str, Any]]:
        """Filter out chain restaurants and big companies - focus on local businesses"""
        
        # Chain keywords from archive + ones we've seen slip through
        chain_keywords = [
            # Fast food chains
            'mcdonald', 'subway', 'taco bell', 'kfc', 'pizza hut', 'domino', 'papa john',
            'wendy', 'burger king', 'chick-fil-a', 'chipotle', 'panera', 'five guys',
            'starbucks', 'dunkin', 'tim horton', 'dairy queen', 'sonic drive',
            'little caesars', 'popeyes', 'arby', 'jack in the box', 'whataburger',
            
            # Pizza chains
            'pizza hut', 'domino', 'papa john', 'little caesars', 'papa murphy',
            'godfather', 'casey', 'hunt brothers pizza',
            
            # Casual dining chains  
            'applebee', 'olive garden', 'red lobster', 'outback steakhouse', 'chili',
            'tgi friday', 'buffalo wild wing', 'cracker barrel', 'ihop', 'denny',
            'waffle house', 'perkins', 'bob evan', 'golden corral', 'ruth chris',
            'longhorn steakhouse', 'texas roadhouse',
            
            # Specific chains we've seen
            'mellow mushroom', 'bonefish grill', 'firehouse subs', 'zaxby', 'moe',
            'california dreaming', 'carolina ale house',
            
            # Coffee chains
            'starbucks', 'dunkin', 'tim hortons', 'caribou coffee',
            
            # Gas stations / convenience  
            'shell', 'exxon', 'bp', 'chevron', 'mobil', '7-eleven', 'circle k',
            'sheetz', 'wawa', 'speedway',
            
            # Grocery/retail chains
            'walmart', 'target', 'kroger', 'safeway', 'cvs', 'walgreens', 'rite aid',
            'food lion', 'harris teeter', 'bi-lo',
            
            # Hotels
            'marriott', 'hilton', 'holiday inn', 'hampton inn', 'best western', 'motel 6',
            'comfort inn', 'quality inn', 'super 8'
        ]
        
        filtered_businesses = []
        for business in businesses:
            business_name = business.get('name', '').lower()
            
            # Skip if it matches any chain keyword
            if any(keyword in business_name for keyword in chain_keywords):
                logger.debug(f"Filtered out chain: {business.get('name')}")
                continue
            
            filtered_businesses.append(business)
            
            if len(filtered_businesses) >= max_results:
                break
        
        logger.info(f"Filtered {len(businesses) - len(filtered_businesses)} chain businesses, kept {len(filtered_businesses)} local businesses")
        return filtered_businesses
    
    def _classify_website(self, website: Optional[str]) -> WebsiteStatus:
        """Classify website status - same as archive version"""
        if not website:
            return WebsiteStatus.NO_WEBSITE
        
        website_lower = website.lower()
        
        # Check for Facebook pages
        facebook_domains = ['facebook.com', 'm.facebook.com']
        for domain in facebook_domains:
            if domain in website_lower:
                return WebsiteStatus.FACEBOOK_ONLY
        
        # Check for Google business sites
        if website_lower.endswith('.business.site'):
            return WebsiteStatus.FACEBOOK_ONLY
        
        return WebsiteStatus.HAS_WEBSITE