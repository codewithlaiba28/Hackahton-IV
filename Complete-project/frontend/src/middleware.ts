import authConfig from '@/lib/auth';
import NextAuth from 'next-auth';
import { NextResponse } from 'next/server';

// Extend authConfig with middleware-specific config
const { auth } = NextAuth(authConfig);

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const isOnDashboard = req.nextUrl.pathname.startsWith('/dashboard');
  const isOnCourse = req.nextUrl.pathname.startsWith('/course');
  const isOnProgress = req.nextUrl.pathname.startsWith('/progress');
  const isOnSettings = req.nextUrl.pathname.startsWith('/settings');
  const isOnLearningPath = req.nextUrl.pathname.startsWith('/learning-path');

  const isProtectedRoute = isOnDashboard || isOnCourse || isOnProgress || isOnSettings || isOnLearningPath;

  if (isProtectedRoute && !isLoggedIn) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  return NextResponse.next();
});

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/course/:path*',
    '/progress/:path*',
    '/settings/:path*',
    '/learning-path/:path*',
  ],
};
