import { useEffect } from 'react'
import { useRouter } from 'next/router'
import Layout from '@/components/Layout'
import { ChevronRightIcon } from '@heroicons/react/24/outline'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token')
    if (token) {
      router.push('/dashboard')
    }
  }, [router])


  return (
    <Layout>
      <div className="min-h-screen">
        {/* Hero Section */}
        <div className="relative overflow-hidden">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:pb-28 xl:pb-32">
              <main className="mx-auto mt-10 max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
                <div className="text-center animate-fade-in">
                  <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl md:text-6xl lg:text-7xl">
                    <span className="block font-display">Transform</span>
                    <span className="block gradient-text font-display">Local Business</span>
                    <span className="block font-display">with AI</span>
                  </h1>
                  <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-gray-600 sm:text-xl">
                    Discover businesses without websites and generate stunning, professional sites in minutes using advanced AI research and beautiful templates.
                  </p>
                  <div className="mx-auto mt-8 flex max-w-md justify-center space-x-4">
                    <button 
                      onClick={() => router.push('/login')}
                      className="button-primary flex items-center space-x-2"
                    >
                      <span>Login</span>
                      <ChevronRightIcon className="h-5 w-5" />
                    </button>
                    <button 
                      onClick={() => router.push('/dashboard')}
                      className="button-secondary flex items-center space-x-2"
                    >
                      <span>View Demo</span>
                    </button>
                  </div>
                </div>
              </main>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="card p-8 text-center">
              <div className="mx-auto h-16 w-16 text-primary-600 mb-4">
                <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Business Discovery</h3>
              <p className="text-gray-600">Find local businesses without websites using intelligent search</p>
            </div>
            <div className="card p-8 text-center">
              <div className="mx-auto h-16 w-16 text-primary-600 mb-4">
                <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Professional Templates</h3>
              <p className="text-gray-600">Beautiful, responsive website templates for every business type</p>
            </div>
            <div className="card p-8 text-center">
              <div className="mx-auto h-16 w-16 text-primary-600 mb-4">
                <svg className="w-full h-full" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Instant Generation</h3>
              <p className="text-gray-600">Generate complete websites in minutes with AI-powered content</p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}

