import { ReactNode } from 'react'
import Head from 'next/head'

interface LayoutProps {
  children: ReactNode
  title?: string
}

export default function Layout({ children, title = 'BizFly' }: LayoutProps) {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content="Generate professional websites for businesses with AI-powered content creation" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
        <meta property="og:title" content="BizFly - AI Website Generator" />
        <meta property="og:description" content="Discover businesses without websites and generate stunning, professional sites automatically" />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </Head>
      
      {/* Background Elements */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50/50 via-purple-50/20 to-accent-50/10" />
        <div className="absolute top-0 left-1/4 w-72 h-72 bg-primary-200/30 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse-soft" />
        <div className="absolute top-0 right-1/4 w-72 h-72 bg-purple-200/30 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse-soft" style={{ animationDelay: '2s' }} />
        <div className="absolute -bottom-8 left-1/3 w-72 h-72 bg-accent-200/30 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse-soft" style={{ animationDelay: '4s' }} />
      </div>
      
      <main className="relative">{children}</main>
    </>
  )
}