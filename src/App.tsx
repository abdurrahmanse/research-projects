import { routes } from '@/routes'
import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import './App.css'

/**
 * App Component
 * Root component that provides routing for the application
 */
function App() {
  // Create browser router with configured routes
  const router = createBrowserRouter(routes)

  return <RouterProvider router={router} />
}

export default App
