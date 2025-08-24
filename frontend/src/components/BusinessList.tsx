import { Business } from '@/types/business'
import { useBusinessStore } from '@/stores/businessStore'
import { Globe, Phone, MapPin, ExternalLink } from 'lucide-react'

interface BusinessListProps {
  onSelectBusiness: (business: Business) => void
  selectedBusiness: Business | null
}

export default function BusinessList({ onSelectBusiness, selectedBusiness }: BusinessListProps) {
  const businesses = useBusinessStore(state => state.businesses)

  const getWebsiteStatusBadge = (status: string) => {
    const badges = {
      no_website: { text: 'No Website', color: 'bg-red-100 text-red-800' },
      facebook_only: { text: 'Facebook Only', color: 'bg-yellow-100 text-yellow-800' },
      has_website: { text: 'Has Website', color: 'bg-green-100 text-green-800' },
    }
    
    const badge = badges[status as keyof typeof badges] || badges.no_website
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${badge.color}`}>
        {badge.text}
      </span>
    )
  }

  if (businesses.length === 0) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-8 text-center">
        <Globe className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <p className="text-gray-500">No businesses found. Try searching for a location.</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-gray-900">
        Found {businesses.length} businesses
      </h3>
      
      <div className="max-h-[600px] overflow-y-auto space-y-3">
        {businesses.map((business) => (
          <div
            key={business.id}
            onClick={() => onSelectBusiness(business)}
            className={`bg-white rounded-lg border p-4 cursor-pointer transition-all ${
              selectedBusiness?.id === business.id
                ? 'border-primary-500 shadow-md'
                : 'border-gray-200 hover:border-gray-300 hover:shadow-sm'
            }`}
          >
            <div className="flex justify-between items-start mb-2">
              <h4 className="font-semibold text-gray-900">{business.name}</h4>
              {getWebsiteStatusBadge(business.website_status)}
            </div>
            
            <div className="space-y-1 text-sm text-gray-600">
              <div className="flex items-center">
                <MapPin className="h-4 w-4 mr-2 text-gray-400" />
                <span className="truncate">{business.address}</span>
              </div>
              
              {business.phone && (
                <div className="flex items-center">
                  <Phone className="h-4 w-4 mr-2 text-gray-400" />
                  <span>{business.phone}</span>
                </div>
              )}
              
              {business.website && (
                <div className="flex items-center">
                  <Globe className="h-4 w-4 mr-2 text-gray-400" />
                  <span className="truncate">{business.website}</span>
                </div>
              )}
            </div>
            
            {business.google_maps_url && (
              <a
                href={business.google_maps_url}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="inline-flex items-center mt-2 text-xs text-primary-600 hover:text-primary-700"
              >
                View on Google Maps
                <ExternalLink className="h-3 w-3 ml-1" />
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}