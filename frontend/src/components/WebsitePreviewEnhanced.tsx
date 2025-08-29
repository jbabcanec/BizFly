import { useState, useEffect, useRef } from 'react'
import { Business } from '@/types/business'
import { useMutation, useQuery } from '@tanstack/react-query'
import { startResearch, generateWebsite, getResearchStatus } from '@/services/api'
import { 
  Loader2, 
  Sparkles, 
  Globe, 
  Zap, 
  CheckCircle2, 
  AlertCircle,
  Clock,
  Search,
  FileText,
  Brain,
  Palette,
  Code,
  Rocket
} from 'lucide-react'

interface WebsitePreviewEnhancedProps {
  business: Business
}

interface ProgressStep {
  id: string
  name: string
  description: string
  icon: React.ReactNode
  progress: number
  status: 'pending' | 'in_progress' | 'completed' | 'error'
  message?: string
}

export default function WebsitePreviewEnhanced({ business }: WebsitePreviewEnhancedProps) {
  const [selectedTemplateId, setSelectedTemplateId] = useState<string | null>(null)
  const [researchSteps, setResearchSteps] = useState<ProgressStep[]>([
    {
      id: 'init',
      name: 'Initializing Research',
      description: 'Setting up AI research agent',
      icon: <Search className="h-5 w-5" />,
      progress: 0,
      status: 'pending'
    },
    {
      id: 'google',
      name: 'Google Search',
      description: 'Searching for business information online',
      icon: <Globe className="h-5 w-5" />,
      progress: 0,
      status: 'pending'
    },
    {
      id: 'social',
      name: 'Social Media Analysis',
      description: 'Checking Facebook, Instagram, and other platforms',
      icon: <FileText className="h-5 w-5" />,
      progress: 0,
      status: 'pending'
    },
    {
      id: 'analysis',
      name: 'AI Content Analysis',
      description: 'Analyzing and summarizing gathered information',
      icon: <Brain className="h-5 w-5" />,
      progress: 0,
      status: 'pending'
    }
  ])

  const [generationSteps, setGenerationSteps] = useState<ProgressStep[]>([
    {
      id: 'template',
      name: 'Template Processing',
      description: 'Loading and customizing selected template',
      icon: <Palette className="h-5 w-5" />,
      progress: 0,
      status: 'pending'
    },
    {
      id: 'content',
      name: 'Content Generation',
      description: 'AI generating website content',
      icon: <Code className="h-5 w-5" />,
      progress: 0,
      status: 'pending'
    },
    {
      id: 'optimization',
      name: 'SEO Optimization',
      description: 'Optimizing for search engines',
      icon: <Rocket className="h-5 w-5" />,
      progress: 0,
      status: 'pending'
    }
  ])

  const [researchCompleted, setResearchCompleted] = useState(false)
  const [generationCompleted, setGenerationCompleted] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)
  const clientId = useRef(`client-${Date.now()}`).current

  // Check existing research status
  const { data: researchStatus } = useQuery({
    queryKey: ['research', business.id],
    queryFn: () => getResearchStatus(business.id),
    refetchInterval: researchCompleted ? false : 2000 // Poll every 2s until completed
  })

  useEffect(() => {
    // Check if research is already completed
    if (researchStatus?.status === 'completed') {
      setResearchCompleted(true)
      setResearchSteps(steps => steps.map(step => ({
        ...step,
        progress: 100,
        status: 'completed'
      })))
    }
  }, [researchStatus])

  // Set up WebSocket connection
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`)
    
    ws.onopen = () => {
      console.log('WebSocket connected')
      // Subscribe to this business
      ws.send(JSON.stringify({
        type: 'subscribe',
        business_id: business.id
      }))
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      if (data.type === 'research_progress') {
        handleResearchProgress(data)
      } else if (data.type === 'generation_progress') {
        handleGenerationProgress(data)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    wsRef.current = ws

    return () => {
      ws.close()
    }
  }, [business.id])

  const handleResearchProgress = (data: any) => {
    setResearchSteps(steps => steps.map(step => {
      if (step.id === data.step) {
        return {
          ...step,
          progress: data.progress,
          status: data.progress === 100 ? 'completed' : 'in_progress',
          message: data.message
        }
      }
      // If this step is in progress, mark previous steps as completed
      const currentIndex = steps.findIndex(s => s.id === data.step)
      const stepIndex = steps.findIndex(s => s.id === step.id)
      if (stepIndex < currentIndex && step.status === 'pending') {
        return { ...step, progress: 100, status: 'completed' }
      }
      return step
    }))

    if (data.status === 'completed') {
      setResearchCompleted(true)
    }
  }

  const handleGenerationProgress = (data: any) => {
    setGenerationSteps(steps => steps.map(step => {
      if (step.id === data.step) {
        return {
          ...step,
          progress: data.progress,
          status: data.progress === 100 ? 'completed' : 'in_progress',
          message: data.message
        }
      }
      // If this step is in progress, mark previous steps as completed
      const currentIndex = steps.findIndex(s => s.id === data.step)
      const stepIndex = steps.findIndex(s => s.id === step.id)
      if (stepIndex < currentIndex && step.status === 'pending') {
        return { ...step, progress: 100, status: 'completed' }
      }
      return step
    }))

    if (data.status === 'completed') {
      setGenerationCompleted(true)
    }
  }

  const researchMutation = useMutation({
    mutationFn: () => startResearch(business.id),
    onMutate: () => {
      // Start first step
      setResearchSteps(steps => steps.map((step, index) => ({
        ...step,
        status: index === 0 ? 'in_progress' : 'pending'
      })))
    }
  })

  const generateMutation = useMutation({
    mutationFn: () => generateWebsite({
      business_id: business.id,
      template_id: selectedTemplateId || 'default',
    }),
    onMutate: () => {
      // Start first generation step
      setGenerationSteps(steps => steps.map((step, index) => ({
        ...step,
        status: index === 0 ? 'in_progress' : 'pending'
      })))
    }
  })

  const handleStartResearch = () => {
    researchMutation.mutate()
  }

  const handleGenerateWebsite = () => {
    if (!researchCompleted) {
      alert('Please complete the research phase first!')
      return
    }
    if (!selectedTemplateId) {
      alert('Please select a template first!')
      return
    }
    generateMutation.mutate()
  }

  const templates = [
    { id: 'minimal', name: 'Minimal', description: 'Clean and simple' },
    { id: 'modern', name: 'Modern', description: 'Contemporary design' },
    { id: 'elegant', name: 'Elegant', description: 'Sophisticated style' },
    { id: 'bold', name: 'Bold', description: 'Eye-catching design' }
  ]

  const overallResearchProgress = researchSteps.reduce((acc, step) => acc + step.progress, 0) / researchSteps.length
  const overallGenerationProgress = generationSteps.reduce((acc, step) => acc + step.progress, 0) / generationSteps.length

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-purple-600 text-white p-6">
        <h3 className="text-xl font-bold mb-2">
          AI Website Generation Pipeline
        </h3>
        <p className="text-primary-100">
          Transform {business.name} with a professional website
        </p>
      </div>

      {/* Business Info */}
      <div className="bg-gray-50 border-b border-gray-200 p-4">
        <div className="flex items-start space-x-4">
          <div className="flex-1">
            <h4 className="font-semibold text-gray-900">{business.name}</h4>
            <p className="text-sm text-gray-600">{business.address}</p>
            {business.phone && (
              <p className="text-sm text-gray-600">{business.phone}</p>
            )}
          </div>
          <div className="text-right">
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
              business.website_status === 'no_website' 
                ? 'bg-red-100 text-red-800'
                : 'bg-yellow-100 text-yellow-800'
            }`}>
              {business.website_status === 'no_website' ? 'No Website' : 'Facebook Only'}
            </span>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Phase 1: Research */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h5 className="text-lg font-semibold text-gray-900 flex items-center">
              <Sparkles className="h-5 w-5 mr-2 text-primary-600" />
              Phase 1: AI Research & Discovery
            </h5>
            {researchCompleted && (
              <CheckCircle2 className="h-5 w-5 text-green-500" />
            )}
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4 space-y-3">
            {researchSteps.map((step) => (
              <div key={step.id} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${
                      step.status === 'completed' ? 'bg-green-100 text-green-600' :
                      step.status === 'in_progress' ? 'bg-blue-100 text-blue-600' :
                      'bg-gray-100 text-gray-400'
                    }`}>
                      {step.icon}
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">{step.name}</p>
                      <p className="text-xs text-gray-500">{step.description}</p>
                      {step.message && (
                        <p className="text-xs text-blue-600 mt-1">{step.message}</p>
                      )}
                    </div>
                  </div>
                  <div className="text-right">
                    {step.status === 'completed' ? (
                      <CheckCircle2 className="h-5 w-5 text-green-500" />
                    ) : step.status === 'in_progress' ? (
                      <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
                    ) : (
                      <Clock className="h-5 w-5 text-gray-300" />
                    )}
                  </div>
                </div>
                {step.status === 'in_progress' && (
                  <div className="ml-11">
                    <div className="bg-gray-200 rounded-full h-2 overflow-hidden">
                      <div 
                        className="bg-blue-500 h-full rounded-full transition-all duration-500"
                        style={{ width: `${step.progress}%` }}
                      />
                    </div>
                    <p className="text-xs text-gray-500 mt-1">{step.progress}% complete</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {!researchCompleted && (
            <button
              onClick={handleStartResearch}
              disabled={researchMutation.isPending}
              className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-primary-600 to-purple-600 hover:from-primary-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {researchMutation.isPending ? (
                <>
                  <Loader2 className="animate-spin h-5 w-5 mr-2" />
                  Research in Progress ({Math.round(overallResearchProgress)}%)
                </>
              ) : (
                <>
                  <Sparkles className="h-5 w-5 mr-2" />
                  Start AI Research
                </>
              )}
            </button>
          )}

          {researchCompleted && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center">
                <CheckCircle2 className="h-5 w-5 text-green-500 mr-2" />
                <div>
                  <p className="font-medium text-green-900">Research Complete!</p>
                  <p className="text-sm text-green-700">
                    Successfully gathered information about {business.name}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Phase 2: Template Selection */}
        <div className={`space-y-4 ${!researchCompleted ? 'opacity-50 pointer-events-none' : ''}`}>
          <h5 className="text-lg font-semibold text-gray-900 flex items-center">
            <Palette className="h-5 w-5 mr-2 text-primary-600" />
            Phase 2: Choose Template
          </h5>
          
          <div className="grid grid-cols-2 gap-3">
            {templates.map((template) => (
              <button
                key={template.id}
                onClick={() => setSelectedTemplateId(template.id)}
                disabled={!researchCompleted}
                className={`p-4 rounded-lg border-2 text-left transition-all ${
                  selectedTemplateId === template.id
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                }`}
              >
                <p className="font-medium text-gray-900">{template.name}</p>
                <p className="text-xs text-gray-500">{template.description}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Phase 3: Generation */}
        <div className={`space-y-4 ${!researchCompleted || !selectedTemplateId ? 'opacity-50 pointer-events-none' : ''}`}>
          <div className="flex items-center justify-between">
            <h5 className="text-lg font-semibold text-gray-900 flex items-center">
              <Zap className="h-5 w-5 mr-2 text-primary-600" />
              Phase 3: Generate Website
            </h5>
            {generationCompleted && (
              <CheckCircle2 className="h-5 w-5 text-green-500" />
            )}
          </div>

          {generateMutation.isPending && (
            <div className="bg-gray-50 rounded-lg p-4 space-y-3">
              {generationSteps.map((step) => (
                <div key={step.id} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-lg ${
                        step.status === 'completed' ? 'bg-green-100 text-green-600' :
                        step.status === 'in_progress' ? 'bg-blue-100 text-blue-600' :
                        'bg-gray-100 text-gray-400'
                      }`}>
                        {step.icon}
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">{step.name}</p>
                        <p className="text-xs text-gray-500">{step.description}</p>
                        {step.message && (
                          <p className="text-xs text-blue-600 mt-1">{step.message}</p>
                        )}
                      </div>
                    </div>
                    <div className="text-right">
                      {step.status === 'completed' ? (
                        <CheckCircle2 className="h-5 w-5 text-green-500" />
                      ) : step.status === 'in_progress' ? (
                        <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
                      ) : (
                        <Clock className="h-5 w-5 text-gray-300" />
                      )}
                    </div>
                  </div>
                  {step.status === 'in_progress' && (
                    <div className="ml-11">
                      <div className="bg-gray-200 rounded-full h-2 overflow-hidden">
                        <div 
                          className="bg-green-500 h-full rounded-full transition-all duration-500"
                          style={{ width: `${step.progress}%` }}
                        />
                      </div>
                      <p className="text-xs text-gray-500 mt-1">{step.progress}% complete</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
          
          <button
            onClick={handleGenerateWebsite}
            disabled={!researchCompleted || !selectedTemplateId || generateMutation.isPending}
            className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {generateMutation.isPending ? (
              <>
                <Loader2 className="animate-spin h-5 w-5 mr-2" />
                Generating Website ({Math.round(overallGenerationProgress)}%)
              </>
            ) : (
              <>
                <Zap className="h-5 w-5 mr-2" />
                Generate Professional Website
              </>
            )}
          </button>

          {!researchCompleted && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
              <div className="flex items-center">
                <AlertCircle className="h-5 w-5 text-yellow-600 mr-2 flex-shrink-0" />
                <p className="text-sm text-yellow-800">
                  Complete research phase first to unlock website generation
                </p>
              </div>
            </div>
          )}

          {researchCompleted && !selectedTemplateId && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <div className="flex items-center">
                <AlertCircle className="h-5 w-5 text-blue-600 mr-2 flex-shrink-0" />
                <p className="text-sm text-blue-800">
                  Please select a template design above
                </p>
              </div>
            </div>
          )}
        </div>

        {generationCompleted && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <CheckCircle2 className="h-5 w-5 text-green-500 mr-2" />
                <div>
                  <p className="font-medium text-green-900">Website Generated Successfully!</p>
                  <p className="text-sm text-green-700">
                    Your professional website for {business.name} is ready
                  </p>
                </div>
              </div>
              <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium">
                View Website →
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}