import axios from 'axios'
import { Business, BusinessSearch, Research } from '@/types/business'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export async function searchBusinesses(params: BusinessSearch): Promise<Business[]> {
  const response = await api.post('/businesses/search', params)
  return response.data
}

export async function getBusiness(id: string): Promise<Business> {
  const response = await api.get(`/businesses/${id}`)
  return response.data
}

export async function listBusinesses(params?: {
  skip?: number
  limit?: number
  website_status?: string
}): Promise<Business[]> {
  const response = await api.get('/businesses', { params })
  return response.data
}

export async function startResearch(businessId: string): Promise<Research> {
  const response = await api.post(`/research/${businessId}/start`)
  return response.data
}

export async function getResearch(businessId: string): Promise<Research> {
  const response = await api.get(`/research/${businessId}`)
  return response.data
}

export const getResearchStatus = getResearch // Alias for compatibility

export async function generateWebsite(params: {
  business_id: string
  template_id: string
}): Promise<any> {
  const response = await api.post('/websites/generate', params)
  return response.data
}

export async function getWebsite(id: string): Promise<any> {
  const response = await api.get(`/websites/${id}`)
  return response.data
}

export async function getBusinessWebsites(businessId: string): Promise<any[]> {
  const response = await api.get(`/websites/business/${businessId}`)
  return response.data
}