import { useState } from "react"
import { useAuth } from "../../context/AuthContext"
import { useNavigate } from "react-router-dom"
const LoginForm = () => {
    // Track form data 
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    })
    const [isSubmitting, setIsSubmitting] = useState(false)
    
    const [error, setError] = useState('')

    // Define submit function
    const { login } = useAuth()

    const navigate = useNavigate()

    const handleChange = (e) => {
        const {name, value} = e.target
        console.log(name, value)
        setFormData(prev => ({
            ...prev,
            [name]: value
        }))
    }

    const handleSubmit = async (e) => {
        setIsSubmitting(true)
        e.preventDefault()
        setError('')
        try {
            await login(formData.username, formData.password)
            navigate('/home'); // Redirect after successful login   
        } 
    catch (error) {
        setError('Login failed. Please check your credentials.');
    } finally {
        setIsSubmitting(false);
       
    }
}
  return (
    <div>
        <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                    {error}
                </div>
            )}
            
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
                <input 
                    type="text" 
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    placeholder="Enter your username"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    required
                />
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                <input 
                    type="password" 
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Enter your password" 
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    required
                />
            </div>
            
            <button 
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            > 
                {isSubmitting ? 'Signing in...' : 'Sign In'}
            </button>
        </form>
    </div>
  )
}

export default LoginForm