import { useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import { useNavigate } from 'react-router-dom' 
const SignUpForm = () => {
    const [formData, setFormData] = useState ({
        username: '',
        password: ''}
    )
    const [isSubmitting, setIsSubmitting] = useState(false)
    const [error, setError] = useState('');
    // call our registration service from auth 
    const { register } = useAuth()
    const navigate = useNavigate()

    const handleChange = (e) => {
        // extract name and values from the event
        const {name, value} = e.target
        // spread previous data and upate state
        setFormData((prev) => ({
            ...prev,
            [name] : value
        }))
    }
    
    const handleSubmit = async (e) => {
        e.preventDefault()
        setIsSubmitting(true)
        setError('')
        
        try {
            await register(formData.username, formData.password)
            // Registration successful, user is now logged in
            navigate('/home'); // Redirect after successful login

        } catch (error) {
            setError(error.message || 'Registration failed. Please try again.');
        } finally {
        setIsSubmitting(false);
    }
        // pass in our state values into it

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
                    placeholder="Enter your username"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    required
                />
            </div>
            
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                <input 
                    type="password"
                    placeholder="Enter your password" 
                    name="password" 
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    required
                />
            </div>
            
            <button 
                type="submit" 
                disabled={isSubmitting}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
                {isSubmitting ? 'Creating Account...' : 'Create Account'}
            </button>
        </form>
    </div>
  )
}

export default SignUpForm