// import './index.css' 
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import LoginPage from './pages/auth/LoginPage'
import SignUpPage from './pages/auth/SignUpPage'
import HomePage from './pages/dashboard/HomePage'
import ProtectedRoute from './components/auth/ProtectedRoute'
import LandingPage from './pages/LandingPage'
import PlanPage from './pages/plan/PlanPage'
function App() {

  return (  
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path='/' element ={ < LandingPage />} />
          <Route path='/login' element ={ < LoginPage />} />
          <Route path='/signup' element ={ < SignUpPage />} />
          {/* Protected Routes */}
          <Route 
            path='/home' 
            element={
              <ProtectedRoute>
                  < HomePage /> 
                </ProtectedRoute>
              } />
          <Route 
            path='/plan' 
            element={
              <ProtectedRoute>
                  < PlanPage /> 
                </ProtectedRoute>
              } />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
