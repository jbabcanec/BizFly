import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import Layout from '@/components/Layout'
import SearchPanel from '@/components/SearchPanel'
import BusinessResults from '@/components/BusinessResults'
import WebsitePreviewEnhanced from '@/components/WebsitePreviewEnhanced'
import { Business } from '@/types/business'
import { 
  MagnifyingGlassIcon, 
  DocumentTextIcon, 
  GlobeAltIcon,
  ArrowRightOnRectangleIcon,
  UserIcon
} from '@heroicons/react/24/outline'

export default function Dashboard() {
  const [selectedBusiness, setSelectedBusiness] = useState<Business | null>(null)
  const [activeTab, setActiveTab] = useState<'search' | 'templates' | 'websites'>('search')
  const [user, setUser] = useState<any>(null)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    
    if (!token || !userData) {
      router.push('/login')
      return
    }

    try {
      setUser(JSON.parse(userData))
    } catch (error) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  const tabs = [
    { id: 'search', label: 'Search Businesses', icon: MagnifyingGlassIcon },
    { id: 'templates', label: 'Templates', icon: DocumentTextIcon },
    { id: 'websites', label: 'Generated Sites', icon: GlobeAltIcon },
  ] as const

  if (!user) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout title="Dashboard - BizFly">
      <div className="min-h-screen">
        {/* Header */}
        <header className="bg-white/80 backdrop-blur-md border-b border-gray-200/50 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <h1 className="text-2xl font-bold gradient-text">BizFly</h1>
                <span className="ml-4 text-gray-600">Dashboard</span>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <UserIcon className="h-4 w-4" />
                  <span>Welcome, <span className="font-semibold">{user.username}</span></span>
                </div>
                <button
                  onClick={handleLogout}
                  className="button-secondary text-sm px-4 py-2 flex items-center space-x-2"
                >
                  <ArrowRightOnRectangleIcon className="h-4 w-4" />
                  <span>Logout</span>
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Navigation Tabs */}
          <div className="glass rounded-3xl p-2 shadow-medium mb-8 max-w-2xl mx-auto">
            <nav className="flex space-x-2" aria-label="Tabs">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`${
                      activeTab === tab.id
                        ? 'bg-white shadow-soft text-primary-700 font-semibold'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-white/50'
                    } flex-1 flex items-center justify-center space-x-2 rounded-2xl px-4 py-3 text-sm font-medium transition-all duration-300 transform hover:scale-[1.02]`}
                  >
                    <Icon className="h-5 w-5" />
                    <span className="hidden sm:block">{tab.label}</span>
                  </button>
                )
              })}
            </nav>
          </div>

          {/* Content Area */}
          <div className="stagger-animation">
            {activeTab === 'search' && (
              <div className="space-y-8">
                {/* Search Panel - Compact but prominent */}
                <div className="bg-gradient-to-br from-white to-gray-50 rounded-3xl p-8 border-2 border-gray-100 shadow-xl">
                  <SearchPanel />
                </div>
                
                {/* MAIN RESULTS SECTION - Full width and prominent */}
                <div id="search-results" className="space-y-6">
                  <BusinessResults 
                    onSelectBusiness={setSelectedBusiness}
                    selectedBusiness={selectedBusiness}
                  />
                </div>
                
                {/* Website Preview - Only show if business is selected, as overlay */}
                {selectedBusiness && (
                  <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-3xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
                      <div className="flex items-center justify-between p-6 border-b border-gray-200 bg-gray-50">
                        <h3 className="text-xl font-semibold text-gray-900">
                          Generate Website for {selectedBusiness.name}
                        </h3>
                        <button 
                          onClick={() => setSelectedBusiness(null)}
                          className="text-gray-400 hover:text-gray-600 p-2 hover:bg-gray-100 rounded-full"
                        >
                          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        </button>
                      </div>
                      <div className="p-6 max-h-[calc(90vh-120px)] overflow-y-auto">
                        <WebsitePreviewEnhanced business={selectedBusiness} />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
            
            {activeTab === 'templates' && (
              <TemplateShowcase />
            )}
            
            {activeTab === 'websites' && (
              <WebsiteManager />
            )}
          </div>
        </main>
      </div>
    </Layout>
  )
}

// Template Showcase Component
function TemplateShowcase() {
  const templates = [
    {
      id: 1,
      name: 'Minimal Professional',
      description: 'Clean, minimal design perfect for service businesses',
      preview: '/templates/minimal-preview.jpg',
      features: ['Responsive Design', 'Contact Forms', 'SEO Optimized'],
      color: 'from-blue-500 to-cyan-500'
    },
    {
      id: 2,
      name: 'Modern Creative',
      description: 'Bold, modern design with animations and gradients',
      preview: '/templates/modern-preview.jpg',
      features: ['Smooth Animations', 'Gallery Support', 'Modern Layout'],
      color: 'from-purple-500 to-pink-500'
    },
    {
      id: 3,
      name: 'Luxury Business',
      description: 'Premium design for high-end businesses',
      preview: '/templates/luxury-preview.jpg',
      features: ['Luxury Design', 'Premium Animations', 'Gold Accents'],
      color: 'from-amber-500 to-orange-500'
    },
  ]

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Website Templates</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">Choose from our collection of professionally designed templates</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {templates.map((template) => (
          <div key={template.id} className="card-interactive group">
            <div className={`h-48 bg-gradient-to-br ${template.color} rounded-t-2xl relative overflow-hidden`}>
              <div className="absolute inset-0 bg-black/10 group-hover:bg-black/5 transition-colors" />
              <div className="absolute bottom-4 left-4 right-4">
                <div className="bg-white/90 backdrop-blur-sm rounded-xl p-3">
                  <div className="h-2 bg-gray-200 rounded mb-2" />
                  <div className="h-2 bg-gray-200 rounded w-3/4 mb-2" />
                  <div className="h-2 bg-gray-200 rounded w-1/2" />
                </div>
              </div>
            </div>
            <div className="p-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">{template.name}</h3>
              <p className="text-gray-600 mb-4">{template.description}</p>
              <div className="flex flex-wrap gap-2 mb-4">
                {template.features.map((feature) => (
                  <span key={feature} className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                    {feature}
                  </span>
                ))}
              </div>
              <button className="w-full button-secondary text-center">
                Use Template
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Import WebsiteManager component
import dynamic from 'next/dynamic'

// Dynamically import WebsiteManager to avoid SSR issues
const WebsiteManager = dynamic(() => import('@/components/WebsiteManager'), {
  ssr: false,
  loading: () => (
    <div className="flex justify-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>
  )
})