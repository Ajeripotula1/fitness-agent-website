
import { useNavigate } from 'react-router-dom'

const LandingPage = () => {
    const navigate = useNavigate()
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8 text-center">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">FitAgent</h1>
          <p className="text-gray-600">Your AI-powered fitness companion</p>
        </div>
        
        <div className="mb-8">
          <div className="text-6xl mb-4">💪</div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Get Your Personalized Fitness Plan</h2>
          <p className="text-gray-600">AI-generated workouts and meal plans tailored just for you</p>
        </div>

        <div className="space-y-3">
          <button 
            onClick={() => { navigate('/signup') }}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Get Started
          </button>
          <button 
            onClick={() => { navigate('/login') }}
            className="w-full bg-gray-100 text-gray-700 py-3 px-6 rounded-lg font-medium hover:bg-gray-200 transition-colors"
          >
            Already have an account? Login
          </button>
        </div>
      </div>
    </div>
  )
}

export default LandingPage