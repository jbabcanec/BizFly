import { useState, useMemo } from 'react'
import dynamic from 'next/dynamic'
import { Business } from '@/types/business'
import { useBusinessStore } from '@/stores/businessStore'
import { 
  Globe, 
  Phone, 
  MapPin, 
  ExternalLink, 
  Filter,
  LayoutGrid,
  LayoutList,
  Map as MapIcon,
  Download,
  Star,
  Clock,
  Users,
  DollarSign,
  Search,
  X
} from 'lucide-react'

// Dynamic import for map to avoid SSR issues
const BusinessMap = dynamic(() => import('./BusinessMap'), {
  ssr: false,
  loading: () => (
    <div className="bg-gray-50 rounded-xl p-8 text-center">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
      <p className="text-gray-600">Loading map...</p>
    </div>
  )
})

interface BusinessResultsProps {
  onSelectBusiness: (business: Business) => void
  selectedBusiness: Business | null
}

type ViewMode = 'list' | 'grid' | 'map'
type FilterType = 'all' | 'no_website' | 'facebook_only' | 'has_website'

export default function BusinessResults({ onSelectBusiness, selectedBusiness }: BusinessResultsProps) {
  const businesses = useBusinessStore(state => state.businesses)
  const [viewMode, setViewMode] = useState<ViewMode>('list')
  const [filterType, setFilterType] = useState<FilterType>('no_website')
  const [searchTerm, setSearchTerm] = useState('')
  const [showFilters, setShowFilters] = useState(true)
  const [selectedBusinesses, setSelectedBusinesses] = useState<Set<string>>(new Set())

  // Filter and search businesses
  const filteredBusinesses = useMemo(() => {
    return businesses.filter(business => {
      // Filter by website status
      if (filterType !== 'all' && business.website_status !== filterType) {
        return false
      }
      
      // Search filter
      if (searchTerm) {
        const searchLower = searchTerm.toLowerCase()
        return (
          business.name.toLowerCase().includes(searchLower) ||
          business.address.toLowerCase().includes(searchLower) ||
          business.business_type?.toLowerCase().includes(searchLower)
        )
      }
      
      return true
    })
  }, [businesses, filterType, searchTerm])

  const getWebsiteStatusInfo = (status: string) => {
    const statusInfo = {
      no_website: { 
        text: 'No Website', 
        color: 'bg-red-100 text-red-800 border-red-200',
        icon: '🚫',
        priority: 'High Priority'
      },
      facebook_only: { 
        text: 'Facebook Only', 
        color: 'bg-yellow-100 text-yellow-800 border-yellow-200',
        icon: '📱',
        priority: 'Medium Priority'
      },
      has_website: { 
        text: 'Has Website', 
        color: 'bg-green-100 text-green-800 border-green-200',
        icon: '✅',
        priority: 'Low Priority'
      },
    }
    
    return statusInfo[status as keyof typeof statusInfo] || statusInfo.no_website
  }

  const handleSelectAll = () => {
    if (selectedBusinesses.size === filteredBusinesses.length) {
      setSelectedBusinesses(new Set())
    } else {
      setSelectedBusinesses(new Set(filteredBusinesses.map(b => b.id)))
    }
  }

  const toggleBusinessSelection = (businessId: string) => {
    const newSelected = new Set(selectedBusinesses)
    if (newSelected.has(businessId)) {
      newSelected.delete(businessId)
    } else {
      newSelected.add(businessId)
    }
    setSelectedBusinesses(newSelected)
  }

  const exportSelected = () => {
    const selected = filteredBusinesses.filter(b => selectedBusinesses.has(b.id))
    const csvContent = [
      ['Name', 'Address', 'Phone', 'Website', 'Status', 'Google Maps'],
      ...selected.map(b => [
        b.name,
        b.address,
        b.phone || '',
        b.website || '',
        b.website_status,
        b.google_maps_url || ''
      ])
    ].map(row => row.map(field => `"${field}"`).join(',')).join('\n')
    
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `businesses-${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  }

  if (businesses.length === 0) {
    return (
      <div className="bg-gradient-to-br from-primary-50 to-purple-50 rounded-3xl p-12 text-center border-2 border-primary-100">
        <div className="mx-auto h-32 w-32 text-primary-300 mb-6">
          <Search className="w-full h-full" />
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">🔍 Start Your Business Discovery</h2>
        <p className="text-xl text-gray-600 mb-8">Find local businesses without websites and generate professional sites instantly</p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto mb-8">
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
            <div className="text-3xl mb-3">📍</div>
            <h3 className="font-semibold text-gray-900 mb-2">1. Search Location</h3>
            <p className="text-sm text-gray-600">Enter your city, zip code, or address to find nearby businesses</p>
          </div>
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
            <div className="text-3xl mb-3">🎯</div>
            <h3 className="font-semibold text-gray-900 mb-2">2. Filter Results</h3>
            <p className="text-sm text-gray-600">Focus on businesses without websites - your prime opportunities</p>
          </div>
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
            <div className="text-3xl mb-3">🚀</div>
            <h3 className="font-semibold text-gray-900 mb-2">3. Generate Sites</h3>
            <p className="text-sm text-gray-600">Create professional websites with AI in just minutes</p>
          </div>
        </div>
        
        <div className="text-primary-600 font-medium">
          ⬆️ Use the search form above to get started
        </div>
      </div>
    )
  }

  const statusCounts = businesses.reduce((acc, business) => {
    acc[business.website_status] = (acc[business.website_status] || 0) + 1
    return acc
  }, {} as Record<string, number>)

  return (
    <div className="space-y-6">
      {/* Header with Stats */}
      <div className="bg-gradient-to-r from-primary-50 to-purple-50 rounded-2xl p-6">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Business Discovery Results</h2>
            <p className="text-gray-600 mt-1">Found {businesses.length} businesses • {filteredBusinesses.length} matching filters</p>
          </div>
          
          <div className="flex flex-wrap gap-3">
            <div className="flex items-center space-x-2 text-sm">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <span className="font-medium">{statusCounts.no_website || 0}</span>
              <span className="text-gray-600">No Website</span>
            </div>
            <div className="flex items-center space-x-2 text-sm">
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <span className="font-medium">{statusCounts.facebook_only || 0}</span>
              <span className="text-gray-600">Facebook Only</span>
            </div>
            <div className="flex items-center space-x-2 text-sm">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="font-medium">{statusCounts.has_website || 0}</span>
              <span className="text-gray-600">Has Website</span>
            </div>
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
        <div className="flex items-center space-x-2">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search businesses..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
            />
          </div>

          {/* Filter Toggle */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center space-x-2 px-3 py-2 rounded-lg border text-sm font-medium transition-colors ${
              showFilters 
                ? 'bg-primary-100 border-primary-300 text-primary-700'
                : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Filter className="h-4 w-4" />
            <span>Filter</span>
            {filterType !== 'all' && <div className="w-2 h-2 bg-primary-500 rounded-full"></div>}
          </button>

          {/* Bulk Actions */}
          {selectedBusinesses.size > 0 && (
            <div className="flex items-center space-x-2 pl-4 border-l border-gray-200">
              <span className="text-sm text-gray-600">{selectedBusinesses.size} selected</span>
              <button
                onClick={exportSelected}
                className="flex items-center space-x-1 px-3 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors text-sm"
              >
                <Download className="h-4 w-4" />
                <span>Export</span>
              </button>
            </div>
          )}
        </div>

        <div className="flex items-center space-x-2">
          {/* View Mode Selector */}
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setViewMode('list')}
              className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm transition-colors ${
                viewMode === 'list' 
                  ? 'bg-white shadow-sm text-gray-900' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <LayoutList className="h-4 w-4" />
              <span className="hidden sm:block">List</span>
            </button>
            <button
              onClick={() => setViewMode('grid')}
              className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm transition-colors ${
                viewMode === 'grid' 
                  ? 'bg-white shadow-sm text-gray-900' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <LayoutGrid className="h-4 w-4" />
              <span className="hidden sm:block">Grid</span>
            </button>
            <button
              onClick={() => setViewMode('map')}
              className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm transition-colors ${
                viewMode === 'map' 
                  ? 'bg-white shadow-sm text-gray-900' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <MapIcon className="h-4 w-4" />
              <span className="hidden sm:block">Map</span>
            </button>
          </div>

          {/* Select All */}
          <button
            onClick={handleSelectAll}
            className="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            {selectedBusinesses.size === filteredBusinesses.length ? 'Deselect All' : 'Select All'}
          </button>
        </div>
      </div>

      {/* Filter Panel */}
      {showFilters && (
        <div className="bg-white border border-gray-200 rounded-xl p-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-sm font-medium text-gray-700">Filter by website status:</span>
            {(['all', 'no_website', 'facebook_only', 'has_website'] as const).map((filter) => (
              <button
                key={filter}
                onClick={() => setFilterType(filter)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                  filterType === filter
                    ? 'bg-primary-100 text-primary-700 border border-primary-300'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {filter === 'all' ? 'All Businesses' : getWebsiteStatusInfo(filter).text}
                {filter !== 'all' && (
                  <span className="ml-1 text-xs">({statusCounts[filter] || 0})</span>
                )}
              </button>
            ))}
            {filterType !== 'all' && (
              <button
                onClick={() => setFilterType('all')}
                className="ml-2 p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>
      )}

      {/* Results */}
      {viewMode === 'map' && (
        <BusinessMap
          businesses={filteredBusinesses}
          selectedBusiness={selectedBusiness}
          onSelectBusiness={onSelectBusiness}
        />
      )}

      {(viewMode === 'list' || viewMode === 'grid') && (
        <div className={viewMode === 'grid' ? 'grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4' : 'space-y-3'}>
          {filteredBusinesses.map((business) => {
            const statusInfo = getWebsiteStatusInfo(business.website_status)
            const isSelected = selectedBusinesses.has(business.id)
            
            return (
              <div
                key={business.id}
                className={`bg-white rounded-xl border-2 p-6 cursor-pointer transition-all transform hover:scale-[1.02] ${
                  selectedBusiness?.id === business.id
                    ? 'border-primary-500 shadow-lg ring-2 ring-primary-100'
                    : isSelected
                    ? 'border-blue-300 shadow-md'
                    : 'border-gray-200 hover:border-gray-300 hover:shadow-md'
                }`}
                onClick={() => onSelectBusiness(business)}
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start space-x-3">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={(e) => {
                        e.stopPropagation()
                        toggleBusinessSelection(business.id)
                      }}
                      className="mt-1 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-1">{business.name}</h3>
                      {business.business_type && (
                        <span className="inline-block px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                          {business.business_type}
                        </span>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex flex-col items-end space-y-2">
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${statusInfo.color}`}>
                      <span className="mr-1">{statusInfo.icon}</span>
                      {statusInfo.text}
                    </span>
                    <span className="text-xs text-gray-500">{statusInfo.priority}</span>
                  </div>
                </div>

                {/* Content */}
                <div className="space-y-3">
                  <div className="flex items-start space-x-2">
                    <MapPin className="h-4 w-4 text-gray-400 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-gray-600 flex-1">{business.address}</span>
                  </div>
                  
                  {business.phone && (
                    <div className="flex items-center space-x-2">
                      <Phone className="h-4 w-4 text-gray-400 flex-shrink-0" />
                      <a 
                        href={`tel:${business.phone}`}
                        className="text-sm text-primary-600 hover:text-primary-700"
                        onClick={(e) => e.stopPropagation()}
                      >
                        {business.phone}
                      </a>
                    </div>
                  )}
                  
                  {business.website && (
                    <div className="flex items-center space-x-2">
                      <Globe className="h-4 w-4 text-gray-400 flex-shrink-0" />
                      <a 
                        href={business.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-primary-600 hover:text-primary-700 truncate"
                        onClick={(e) => e.stopPropagation()}
                      >
                        {business.website}
                      </a>
                    </div>
                  )}
                </div>

                {/* Actions */}
                <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
                  {business.google_maps_url && (
                    <a
                      href={business.google_maps_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="inline-flex items-center text-xs text-gray-500 hover:text-gray-700"
                    >
                      <ExternalLink className="h-3 w-3 mr-1" />
                      Google Maps
                    </a>
                  )}
                  
                  <div className="flex items-center justify-end space-x-2">
                    {business.website_status === 'no_website' && (
                      <>
                        <span className="text-xs text-gray-500">Perfect candidate!</span>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            onSelectBusiness(business)
                          }}
                          className="px-3 py-1 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-full text-xs font-medium hover:from-primary-600 hover:to-primary-700 transition-all shadow-sm"
                        >
                          🚀 Generate Website
                        </button>
                      </>
                    )}
                    {business.website_status === 'facebook_only' && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          onSelectBusiness(business)
                        }}
                        className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs font-medium hover:bg-yellow-200 transition-colors"
                      >
                        Upgrade to Website
                      </button>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {filteredBusinesses.length === 0 && businesses.length > 0 && (
        <div className="text-center py-12">
          <Filter className="mx-auto h-16 w-16 text-gray-400 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Results Found</h3>
          <p className="text-gray-600 mb-4">No businesses match your current filters</p>
          <button
            onClick={() => {
              setFilterType('all')
              setSearchTerm('')
            }}
            className="button-secondary"
          >
            Clear Filters
          </button>
        </div>
      )}
    </div>
  )
}