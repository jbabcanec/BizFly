import { useState, useEffect } from 'react'
import { 
  GlobeAltIcon, 
  CodeBracketIcon, 
  ArrowDownTrayIcon,
  RocketLaunchIcon,
  TrashIcon,
  PlayIcon,
  StopIcon,
  EyeIcon,
  PencilSquareIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon
} from '@heroicons/react/24/outline'

interface Website {
  id: string
  businessName: string
  businessId: string
  template: string
  generatedAt: string
  lastModified: string
  status: 'draft' | 'published' | 'archived'
  previewUrl?: string
  previewPort?: number
  isPreviewRunning?: boolean
  thumbnail?: string
  size?: string
}

interface PreviewServer {
  business_id: string
  port: number
  url: string
  started_at: string
  is_running: boolean
}

export default function WebsiteManager() {
  const [websites, setWebsites] = useState<Website[]>([])
  const [activePreview, setActivePreview] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [selectedWebsite, setSelectedWebsite] = useState<Website | null>(null)
  const [showCodeEditor, setShowCodeEditor] = useState(false)

  useEffect(() => {
    fetchWebsites()
  }, [])

  const fetchWebsites = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/websites/list', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          setWebsites(data.websites)
        }
      } else {
        console.error('Failed to fetch websites:', response.statusText)
        // Fallback to empty array
        setWebsites([])
      }
    } catch (error) {
      console.error('Failed to fetch websites:', error)
      setWebsites([])
    } finally {
      setLoading(false)
    }
  }

  const startPreview = async (website: Website) => {
    try {
      const response = await fetch(`/api/websites/${website.businessId}/preview`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          // Update website with preview info
          setWebsites(prev => prev.map(w => 
            w.id === website.id 
              ? { ...w, previewPort: data.preview.port, previewUrl: data.preview.url, isPreviewRunning: true }
              : w
          ))
          setActivePreview(website.id)
          
          // Open preview in new tab
          window.open(data.preview.url, '_blank')
        }
      }
    } catch (error) {
      console.error('Failed to start preview:', error)
    }
  }

  const stopPreview = async (website: Website) => {
    try {
      const response = await fetch(`/api/websites/${website.businessId}/preview`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        setWebsites(prev => prev.map(w => 
          w.id === website.id 
            ? { ...w, previewPort: undefined, previewUrl: undefined, isPreviewRunning: false }
            : w
        ))
        if (activePreview === website.id) {
          setActivePreview(null)
        }
      }
    } catch (error) {
      console.error('Failed to stop preview:', error)
    }
  }

  const downloadWebsite = async (website: Website) => {
    try {
      const response = await fetch(`/api/websites/${website.businessId}/download`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${website.businessName.replace(/\s+/g, '_')}_website.zip`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      }
    } catch (error) {
      console.error('Failed to download website:', error)
    }
  }

  const deleteWebsite = async (website: Website) => {
    if (!confirm(`Are you sure you want to delete the website for ${website.businessName}?`)) {
      return
    }
    
    try {
      const response = await fetch(`/api/websites/${website.businessId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        setWebsites(prev => prev.filter(w => w.id !== website.id))
      }
    } catch (error) {
      console.error('Failed to delete website:', error)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const hours = Math.floor(diff / (1000 * 60 * 60))
    
    if (hours < 1) {
      return 'Just now'
    } else if (hours < 24) {
      return `${hours} hour${hours > 1 ? 's' : ''} ago`
    } else {
      const days = Math.floor(hours / 24)
      return `${days} day${days > 1 ? 's' : ''} ago`
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'published':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />
      case 'draft':
        return <ClockIcon className="h-5 w-5 text-yellow-500" />
      case 'archived':
        return <XCircleIcon className="h-5 w-5 text-gray-400" />
      default:
        return null
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Generated Websites</h2>
          <p className="text-gray-600 mt-2">Manage, preview, and deploy your generated websites</p>
        </div>
        <div className="flex space-x-3">
          <button className="button-secondary">
            <RocketLaunchIcon className="h-5 w-5 mr-2" />
            Deploy All
          </button>
        </div>
      </div>

      {/* Active Preview Banner */}
      {activePreview && (
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <div className="absolute inset-0 bg-green-400 rounded-full animate-ping opacity-50"></div>
                <div className="relative bg-green-500 rounded-full p-2">
                  <PlayIcon className="h-4 w-4 text-white" />
                </div>
              </div>
              <div>
                <p className="font-semibold text-gray-900">Preview Server Active</p>
                <p className="text-sm text-gray-600">
                  {websites.find(w => w.id === activePreview)?.businessName} is running on port {websites.find(w => w.id === activePreview)?.previewPort}
                </p>
              </div>
            </div>
            <button 
              onClick={() => {
                const website = websites.find(w => w.id === activePreview)
                if (website) stopPreview(website)
              }}
              className="text-red-600 hover:text-red-700 font-medium text-sm"
            >
              Stop Preview
            </button>
          </div>
        </div>
      )}

      {/* Websites Grid */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : websites.length === 0 ? (
        <div className="text-center py-12">
          <GlobeAltIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No websites yet</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by generating your first website.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {websites.map((website) => (
            <div key={website.id} className="card-interactive group overflow-hidden">
              {/* Thumbnail */}
              <div className="relative h-48 bg-gradient-to-br from-gray-100 to-gray-200 overflow-hidden">
                {website.thumbnail ? (
                  <img 
                    src={website.thumbnail} 
                    alt={website.businessName}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <GlobeAltIcon className="h-16 w-16 text-gray-400" />
                  </div>
                )}
                
                {/* Status Badge */}
                <div className="absolute top-3 right-3">
                  <div className={`px-3 py-1 rounded-full text-xs font-medium backdrop-blur-sm flex items-center space-x-1 ${
                    website.status === 'published' ? 'bg-green-100/90 text-green-800' :
                    website.status === 'draft' ? 'bg-yellow-100/90 text-yellow-800' :
                    'bg-gray-100/90 text-gray-800'
                  }`}>
                    {getStatusIcon(website.status)}
                    <span className="capitalize">{website.status}</span>
                  </div>
                </div>

                {/* Preview Running Indicator */}
                {website.isPreviewRunning && (
                  <div className="absolute top-3 left-3">
                    <div className="relative">
                      <div className="absolute inset-0 bg-green-400 rounded-full animate-ping"></div>
                      <div className="relative bg-green-500 text-white px-2 py-1 rounded-full text-xs font-medium">
                        Live
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Content */}
              <div className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-1">{website.businessName}</h3>
                <p className="text-sm text-gray-500 mb-3">
                  {website.template} • {website.size}
                </p>
                
                <div className="flex items-center justify-between text-xs text-gray-500 mb-4">
                  <span>Created {formatDate(website.generatedAt)}</span>
                  <span>Modified {formatDate(website.lastModified)}</span>
                </div>

                {/* Action Buttons */}
                <div className="grid grid-cols-2 gap-2">
                  {website.isPreviewRunning ? (
                    <>
                      <button 
                        onClick={() => window.open(website.previewUrl, '_blank')}
                        className="flex items-center justify-center px-3 py-2 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium"
                      >
                        <EyeIcon className="h-4 w-4 mr-1" />
                        View
                      </button>
                      <button 
                        onClick={() => stopPreview(website)}
                        className="flex items-center justify-center px-3 py-2 bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors text-sm font-medium"
                      >
                        <StopIcon className="h-4 w-4 mr-1" />
                        Stop
                      </button>
                    </>
                  ) : (
                    <>
                      <button 
                        onClick={() => startPreview(website)}
                        className="flex items-center justify-center px-3 py-2 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors text-sm font-medium"
                      >
                        <PlayIcon className="h-4 w-4 mr-1" />
                        Preview
                      </button>
                      <button 
                        onClick={() => {
                          setSelectedWebsite(website)
                          setShowCodeEditor(true)
                        }}
                        className="flex items-center justify-center px-3 py-2 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors text-sm font-medium"
                      >
                        <CodeBracketIcon className="h-4 w-4 mr-1" />
                        Edit
                      </button>
                    </>
                  )}
                  
                  <button 
                    onClick={() => downloadWebsite(website)}
                    className="flex items-center justify-center px-3 py-2 bg-gray-50 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors text-sm font-medium"
                  >
                    <ArrowDownTrayIcon className="h-4 w-4 mr-1" />
                    Download
                  </button>
                  
                  <button 
                    onClick={() => deleteWebsite(website)}
                    className="flex items-center justify-center px-3 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors text-sm font-medium"
                  >
                    <TrashIcon className="h-4 w-4 mr-1" />
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Code Editor Modal (placeholder) */}
      {showCodeEditor && selectedWebsite && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
            <div className="flex items-center justify-between p-6 border-b">
              <h3 className="text-xl font-semibold">Code Editor - {selectedWebsite.businessName}</h3>
              <button 
                onClick={() => setShowCodeEditor(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <XCircleIcon className="h-6 w-6" />
              </button>
            </div>
            <div className="p-6">
              <p className="text-gray-600">Code editor coming soon...</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}