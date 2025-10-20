import { useEffect, useState } from 'react'
import { useAuth } from '../../context/AuthContext'
import ProfileForm from '../../components/forms/ProfileForm'
import { profileService } from '../../services/profileService'
import { useNavigate } from 'react-router-dom'
import NavBar from '../../components/ui/NavBar'

const HomePage = () => {
  const { user, logout, token } = useAuth()
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()


  // Fetch Profile on mount
  useEffect(() => {
    loadProfile()
  }, [])

  // Helper function to get Profile information 
  const loadProfile = async () => {
    try {
      const profileData = await profileService.getProfile(token)
      setProfile(profileData)
      setShowForm(!profileData) // Show form if no profile exists
    } catch (error) {
      console.error('Failed to load profile:', error)
      setShowForm(true) // Show form if profile doesn't exist
    } finally {
      setLoading(false)
    }
  }

  // Submit Profile to backend 
  const handleProfileSubmit = async (profileData) => {
    setIsSubmitting(true)
    setError('')
    try {
      const savedProfile = await profileService.createProfile(profileData, token)
      setProfile(savedProfile) // update local state
      setShowForm(false)
    } catch (error) {
      setError(error.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  if (loading) {
    return <div className="p-6">Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <NavBar />
      
      <div className="max-w-4xl mx-auto px-4 md:px-6 py-6 md:py-8">
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.username}! 👋
          </h1>
          <p className="text-gray-600">Manage your fitness profile and track your progress</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {showForm ? (
          <div className="bg-white rounded-xl shadow-lg p-6 md:p-8">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Set Up Your Profile</h2>
              <p className="text-gray-600">Tell us about yourself to get personalized fitness plans</p>
            </div>
            <ProfileForm
              onSubmit={handleProfileSubmit}
              initialData={profile}
              isSubmitting={isSubmitting}
            />
          </div>
        ) : (
          <div className="grid md:grid-cols-2 gap-6">
            {/* Profile Summary Card */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-xl font-bold text-gray-900">Your Profile</h2>
                <button
                  onClick={() => setShowForm(true)}
                  className="text-blue-600 hover:text-blue-700 font-medium transition-colors"
                >
                  Edit
                </button>
              </div>
              
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Age:</span>
                  <span className="font-medium">{profile.age} years</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Weight:</span>
                  <span className="font-medium">{profile.weight} lbs</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Height:</span>
                  <span className="font-medium">{profile.height_feet}'{profile.height_inches}"</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Gender:</span>
                  <span className="font-medium capitalize">{profile.gender}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Goal:</span>
                  <span className="font-medium capitalize">{profile.fitness_goal?.replace('-', ' ')}</span>
                </div>
              </div>
            </div>

            {/* Quick Actions Card */}
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Ready to Start?</h3>
              <p className="text-gray-700 mb-6">Generate your personalized fitness and meal plan based on your profile.</p>
              <button
                onClick={() => navigate('/plan')}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
              >
                View My Plan
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default HomePage