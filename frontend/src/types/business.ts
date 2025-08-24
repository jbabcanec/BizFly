export interface Business {
  id: string
  google_place_id: string
  name: string
  address: string
  latitude: number
  longitude: number
  phone?: string
  website?: string
  website_status: 'no_website' | 'facebook_only' | 'has_website'
  google_maps_url?: string
  business_type?: string
  discovered_at: string
  last_checked: string
}

export interface BusinessSearch {
  location: string
  radius_miles: number
  business_types?: string[]
}

export interface Research {
  id: string
  business_id: string
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  description?: string
  services?: string[]
  hours?: Record<string, string>
  reviews?: any[]
  social_media?: Record<string, string>
  images?: string[]
  menu_items?: any[]
  specialties?: string[]
  history?: string
  owner_info?: any
  researched_at?: string
  updated_at: string
}