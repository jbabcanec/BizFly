import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Search, MapPin, Loader2 } from 'lucide-react'
import { useMutation } from '@tanstack/react-query'
import { searchBusinesses } from '@/services/api'
import { useBusinessStore } from '@/stores/businessStore'

const searchSchema = z.object({
  location: z.string().min(1, 'Location is required'),
  radius: z.number().min(0.1).max(50),
  businessTypes: z.string().optional(),
})

type SearchFormData = z.infer<typeof searchSchema>

export default function SearchPanel() {
  const { register, handleSubmit, formState: { errors } } = useForm<SearchFormData>({
    resolver: zodResolver(searchSchema),
    defaultValues: {
      radius: 5,
    }
  })
  
  const setBusinesses = useBusinessStore(state => state.setBusinesses)
  
  const searchMutation = useMutation({
    mutationFn: searchBusinesses,
    onSuccess: (data) => {
      setBusinesses(data)
      
      // Auto-scroll to results after successful search
      setTimeout(() => {
        const resultsElement = document.getElementById('search-results')
        if (resultsElement) {
          resultsElement.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
          })
        }
      }, 300) // Small delay to ensure results are rendered
    }
  })

  const onSubmit = (data: SearchFormData) => {
    const businessTypes = data.businessTypes 
      ? data.businessTypes.split(',').map(t => t.trim())
      : undefined
      
    searchMutation.mutate({
      location: data.location,
      radius_miles: data.radius,
      business_types: businessTypes
    })
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Discover Local Businesses</h2>
        <p className="text-gray-600">Find businesses without websites and transform them with AI-generated sites</p>
      </div>
      
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="space-y-4">
          <div>
            <label htmlFor="location" className="block text-sm font-semibold text-gray-900 mb-3">
              Location
            </label>
            <div className="relative group">
              <MapPin className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5 group-focus-within:text-primary-500 transition-colors" />
              <input
                {...register('location')}
                type="text"
                placeholder="Enter city, address, or coordinates"
                className="input-field pl-12 py-4 text-lg placeholder-gray-400"
              />
            </div>
            {errors.location && (
              <p className="mt-2 text-sm text-red-600 animate-fade-in">{errors.location.message}</p>
            )}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label htmlFor="radius" className="block text-sm font-semibold text-gray-900 mb-3">
                Search Radius
              </label>
              <div className="relative">
                <input
                  {...register('radius', { valueAsNumber: true })}
                  type="number"
                  step="0.1"
                  min="0.1"
                  max="50"
                  className="input-field py-4"
                />
                <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500 text-sm font-medium">
                  miles
                </span>
              </div>
              {errors.radius && (
                <p className="mt-2 text-sm text-red-600 animate-fade-in">{errors.radius.message}</p>
              )}
            </div>

            <div>
              <label htmlFor="businessTypes" className="block text-sm font-semibold text-gray-900 mb-3">
                Business Types
              </label>
              <input
                {...register('businessTypes')}
                type="text"
                placeholder="restaurant, cafe, store..."
                className="input-field py-4 placeholder-gray-400"
              />
              <p className="mt-1 text-xs text-gray-500">Optional: Comma-separated list</p>
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={searchMutation.isPending}
          className="w-full button-primary py-4 text-lg font-semibold relative overflow-hidden group"
        >
          <div className="relative z-10 flex items-center justify-center">
            {searchMutation.isPending ? (
              <>
                <Loader2 className="animate-spin h-6 w-6 mr-3" />
                <span>Discovering businesses...</span>
              </>
            ) : (
              <>
                <Search className="h-6 w-6 mr-3" />
                <span>Start Discovery</span>
              </>
            )}
          </div>
          {searchMutation.isPending && (
            <div className="absolute inset-0 bg-gradient-to-r from-primary-400 to-primary-600 opacity-75 animate-pulse" />
          )}
        </button>
      </form>

      {searchMutation.isError && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl animate-fade-in">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-semibold text-red-800">Search Error</h3>
              <p className="text-sm text-red-700 mt-1">
                {searchMutation.error?.message || 'Unable to search businesses. Please try again.'}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}