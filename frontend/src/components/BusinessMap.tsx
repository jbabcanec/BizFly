import { useEffect, useMemo } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'
import { Business } from '@/types/business'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix for default markers in react-leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

// Custom markers for different website statuses
const createCustomIcon = (status: string) => {
  const color = status === 'no_website' ? '#ef4444' : 
               status === 'facebook_only' ? '#eab308' : '#22c55e'
  
  return L.divIcon({
    html: `
      <div style="
        background: ${color};
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: white;
        font-size: 12px;
      ">
        ${status === 'no_website' ? '!' : status === 'facebook_only' ? 'F' : '✓'}
      </div>
    `,
    className: 'custom-marker',
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  })
}

interface BusinessMapProps {
  businesses: Business[]
  selectedBusiness: Business | null
  onSelectBusiness: (business: Business) => void
}

// Component to handle map centering
function MapController({ businesses }: { businesses: Business[] }) {
  const map = useMap()
  
  useEffect(() => {
    if (businesses.length > 0) {
      const bounds = L.latLngBounds(
        businesses.map(b => [b.latitude, b.longitude])
      )
      map.fitBounds(bounds, { padding: [20, 20] })
    }
  }, [businesses, map])
  
  return null
}

export default function BusinessMap({ businesses, selectedBusiness, onSelectBusiness }: BusinessMapProps) {
  const center = useMemo(() => {
    if (businesses.length === 0) return [34.0007, -81.0348] // Columbia, SC default
    
    const avgLat = businesses.reduce((sum, b) => sum + b.latitude, 0) / businesses.length
    const avgLng = businesses.reduce((sum, b) => sum + b.longitude, 0) / businesses.length
    return [avgLat, avgLng]
  }, [businesses])

  if (businesses.length === 0) {
    return (
      <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl border-2 border-blue-100 overflow-hidden">
        <div className="p-6 border-b border-blue-200 bg-white/50">
          <h3 className="text-lg font-semibold text-gray-900">🗺️ Interactive Business Map</h3>
          <p className="text-sm text-gray-600 mt-1">Search for businesses to see them plotted with coordinates</p>
        </div>
        <div className="h-[700px] flex items-center justify-center bg-gradient-to-br from-blue-100/30 to-purple-100/30">
          <div className="text-center max-w-md">
            <div className="text-blue-400 mb-6">
              <svg className="mx-auto h-24 w-24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 4m0 13V4m0 0L9 7" />
              </svg>
            </div>
            <h4 className="text-xl font-semibold text-gray-900 mb-3">Ready for Geographic Discovery</h4>
            <p className="text-gray-600 mb-6">Once you search for businesses, they'll appear as color-coded markers on this interactive map</p>
            <div className="flex items-center justify-center space-x-4 text-xs">
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <span>No Website</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <span>Facebook Only</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span>Has Website</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="p-4 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">Business Locations</h3>
          <div className="flex items-center space-x-4 text-xs">
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <span>No Website</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <span>Facebook Only</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>Has Website</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="h-[700px]">
        <MapContainer
          center={center as [number, number]}
          zoom={12}
          className="h-full w-full"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          <MapController businesses={businesses} />
          
          {businesses.map((business) => (
            <Marker
              key={business.id}
              position={[business.latitude, business.longitude]}
              icon={createCustomIcon(business.website_status)}
              eventHandlers={{
                click: () => onSelectBusiness(business),
              }}
            >
              <Popup>
                <div className="p-2">
                  <h4 className="font-semibold text-gray-900 mb-1">{business.name}</h4>
                  <p className="text-sm text-gray-600 mb-2">{business.address}</p>
                  
                  {business.phone && (
                    <p className="text-sm text-gray-600 mb-1">📞 {business.phone}</p>
                  )}
                  
                  <div className="flex items-center justify-between mt-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      business.website_status === 'no_website' ? 'bg-red-100 text-red-800' :
                      business.website_status === 'facebook_only' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-green-100 text-green-800'
                    }`}>
                      {business.website_status === 'no_website' ? 'No Website' :
                       business.website_status === 'facebook_only' ? 'Facebook Only' :
                       'Has Website'}
                    </span>
                  </div>
                  
                  {business.website_status === 'no_website' && (
                    <button
                      onClick={() => onSelectBusiness(business)}
                      className="w-full mt-2 px-3 py-1 bg-primary-500 text-white rounded-lg text-sm hover:bg-primary-600 transition-colors"
                    >
                      🚀 Generate Website
                    </button>
                  )}
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  )
}