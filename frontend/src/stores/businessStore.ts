import { create } from 'zustand'
import { Business } from '@/types/business'

interface BusinessStore {
  businesses: Business[]
  selectedBusiness: Business | null
  setBusinesses: (businesses: Business[]) => void
  selectBusiness: (business: Business | null) => void
  clearBusinesses: () => void
}

export const useBusinessStore = create<BusinessStore>((set) => ({
  businesses: [],
  selectedBusiness: null,
  
  setBusinesses: (businesses) => set({ businesses }),
  
  selectBusiness: (business) => set({ selectedBusiness: business }),
  
  clearBusinesses: () => set({ businesses: [], selectedBusiness: null }),
}))