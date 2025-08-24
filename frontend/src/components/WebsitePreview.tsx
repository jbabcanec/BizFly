import { useState } from 'react'
import { Business } from '@/types/business'
import { useMutation } from '@tanstack/react-query'
import { startResearch, generateWebsite } from '@/services/api'
import { Loader2, Sparkles, Globe, Zap } from 'lucide-react'

interface WebsitePreviewProps {
  business: Business
}

export default function WebsitePreview({ business }: WebsitePreviewProps) {
  const [selectedTemplateId, setSelectedTemplateId] = useState<string | null>(null)

  const researchMutation = useMutation({
    mutationFn: () => startResearch(business.id),
  })

  const generateMutation = useMutation({
    mutationFn: () => generateWebsite({
      business_id: business.id,
      template_id: selectedTemplateId || 'default',
    }),
  })

  const handleStartResearch = () => {
    researchMutation.mutate()
  }

  const handleGenerateWebsite = () => {
    generateMutation.mutate()
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Website Generation
      </h3>

      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <h4 className="font-medium text-gray-900 mb-2">{business.name}</h4>
        <p className="text-sm text-gray-600">{business.address}</p>
        {business.phone && (
          <p className="text-sm text-gray-600">{business.phone}</p>
        )}
      </div>

      <div className="space-y-4">
        <div className="border-t pt-4">
          <h5 className="font-medium text-gray-900 mb-3 flex items-center">
            <Sparkles className="h-5 w-5 mr-2 text-primary-600" />
            Step 1: AI Research
          </h5>
          
          <p className="text-sm text-gray-600 mb-3">
            Our AI agent will research this business online to gather information for the website.
          </p>
          
          <button
            onClick={handleStartResearch}
            disabled={researchMutation.isPending}
            className="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {researchMutation.isPending ? (
              <>
                <Loader2 className="animate-spin h-4 w-4 mr-2" />
                Researching...
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4 mr-2" />
                Start AI Research
              </>
            )}
          </button>
        </div>

        <div className="border-t pt-4">
          <h5 className="font-medium text-gray-900 mb-3 flex items-center">
            <Globe className="h-5 w-5 mr-2 text-primary-600" />
            Step 2: Select Template
          </h5>
          
          <div className="grid grid-cols-2 gap-3 mb-3">
            <button
              onClick={() => setSelectedTemplateId('minimal')}
              className={`p-3 rounded-lg border text-sm ${
                selectedTemplateId === 'minimal'
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              Minimal
            </button>
            <button
              onClick={() => setSelectedTemplateId('modern')}
              className={`p-3 rounded-lg border text-sm ${
                selectedTemplateId === 'modern'
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              Modern
            </button>
          </div>
        </div>

        <div className="border-t pt-4">
          <h5 className="font-medium text-gray-900 mb-3 flex items-center">
            <Zap className="h-5 w-5 mr-2 text-primary-600" />
            Step 3: Generate Website
          </h5>
          
          <button
            onClick={handleGenerateWebsite}
            disabled={!selectedTemplateId || generateMutation.isPending}
            className="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {generateMutation.isPending ? (
              <>
                <Loader2 className="animate-spin h-4 w-4 mr-2" />
                Generating...
              </>
            ) : (
              <>
                <Zap className="h-4 w-4 mr-2" />
                Generate Website
              </>
            )}
          </button>
        </div>
      </div>

      {generateMutation.isSuccess && (
        <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-md">
          <p className="text-sm text-green-800">
            Website generated successfully! View in the Websites tab.
          </p>
        </div>
      )}
    </div>
  )
}