import { withAuth } from 'next-auth/middleware'
import { NextResponse } from 'next/server'

export default withAuth(
  function middleware(req) {
    // Check if user is trying to access admin routes
    if (req.nextUrl.pathname.startsWith('/admin')) {
      const token = req.nextauth.token
      
      // Redirect to login if not authenticated
      if (!token) {
        return NextResponse.redirect(new URL('/auth/signin', req.url))
      }
      
      // Redirect to dashboard if not admin
      if (token.role !== 'ADMIN') {
        return NextResponse.redirect(new URL('/dashboard', req.url))
      }
    }
    
    return NextResponse.next()
  },
  {
    callbacks: {
      authorized: ({ token, req }) => {
        // Allow access to non-admin routes
        if (!req.nextUrl.pathname.startsWith('/admin')) {
          return true
        }
        
        // For admin routes, check if user exists and has admin role
        return !!token && token.role === 'ADMIN'
      },
    },
  }
)

export const config = {
  matcher: ['/admin/:path*', '/dashboard/:path*']
} 