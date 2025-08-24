import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import SearchPanel from '@/components/SearchPanel'

// Mock the API
jest.mock('@/services/api', () => ({
  searchBusinesses: jest.fn()
}))

// Mock the store
jest.mock('@/stores/businessStore', () => ({
  useBusinessStore: jest.fn(() => ({
    setBusinesses: jest.fn()
  }))
}))

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
  
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}

describe('SearchPanel', () => {
  it('renders search form', () => {
    render(<SearchPanel />, { wrapper: createWrapper() })
    
    expect(screen.getByText('Search for Businesses')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Enter address or coordinates')).toBeInTheDocument()
    expect(screen.getByText('Search Businesses')).toBeInTheDocument()
  })

  it('validates required location field', async () => {
    render(<SearchPanel />, { wrapper: createWrapper() })
    
    const submitButton = screen.getByText('Search Businesses')
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(screen.getByText('Location is required')).toBeInTheDocument()
    })
  })

  it('submits form with valid data', async () => {
    const { searchBusinesses } = require('@/services/api')
    searchBusinesses.mockResolvedValue([])
    
    render(<SearchPanel />, { wrapper: createWrapper() })
    
    const locationInput = screen.getByPlaceholderText('Enter address or coordinates')
    const submitButton = screen.getByText('Search Businesses')
    
    fireEvent.change(locationInput, { target: { value: 'New York, NY' } })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(searchBusinesses).toHaveBeenCalledWith({
        location: 'New York, NY',
        radius_miles: 5,
        business_types: undefined
      })
    })
  })
})