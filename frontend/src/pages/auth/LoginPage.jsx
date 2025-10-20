import LoginForm from "../../components/forms/LoginForm"
import { useNavigate } from "react-router-dom"

const LoginPage = () => {
  const navigate = useNavigate()
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome Back</h1>
          <p className="text-gray-600">Sign in to your FitAgent account</p>
        </div>
        
        <LoginForm />
        
        <div className="mt-6 text-center">
          <p className="text-gray-600 mb-3">Don't have an account?</p>
          <button
            onClick={() => { navigate('/signup') }}
            className="text-blue-600 hover:text-blue-700 font-medium transition-colors"
          >
            Create account here
          </button>
        </div>
      </div>
    </div>
  )
}

export default LoginPage