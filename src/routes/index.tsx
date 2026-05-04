import { Portfolio } from '@/pages'
import type { RouteObject } from 'react-router-dom'

/**
 * Route Configuration
 * Central configuration file for all application routes
 */

export const routes: RouteObject[] = [
  {
    path: '/',
    element: <Portfolio />,
    errorElement: null,
  },
  {
    path: '/portfolio',
    element: <Portfolio />,
  },
]

/**
 * App Routes Object
 * Main app route configuration
 */
export const appRoutes: RouteObject = {
  children: routes,
}
