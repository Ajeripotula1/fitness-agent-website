import { useEffect, useState } from 'react'
import { planService } from '../../services/planService'
import { useAuth } from '../../context/AuthContext'
import HealthMetrics from '../../components/plan/HealthMetrics'
import WorkoutPlan from '../../components/plan/WorkoutPlan'
import MealPlan from '../../components/plan/MealPlan'
import { useNavigate } from 'react-router-dom'
import TabButton from '../../components/ui/TabButton'
import NavBar from '../../components/ui/NavBar'

const PlanPage = () => {
    const { token, logout } = useAuth()
    const [plan, setPlan] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [activeTab, setActiveTab] = useState('overview') // 'overview', 'workout', 'meals'

    const navigate = useNavigate()


    const fetchPlan = async () => {
        try {
            setLoading(true)
            setError(null)
            console.log('Fetching plan')
            const planData = await planService.getPlan(token)
            setPlan(planData)
            console.log("Plan data: ", planData)
        } catch (error) {
            console.error('Failed to fetch plan:', error)
            setError(error.message)

        } finally {
            setLoading(false)
        }
    }


    const generatePlan = async () => {
        try {
            setLoading(true)
            setError(null)
            console.log('Generating plan')

            const planData = await planService.generatePlan(token)
            setPlan(planData)
            console.log('Plan data:', planData)
        } catch (error) {
            console.error('Failed to load plan:', error)
            setError(error.message)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchPlan()
    }, [])


    return (
        <div className="max-w-4xl mx-auto px-4 md:px-6 py-6 md:py-8">

            {/* Nav Bar */}
            <NavBar />

            {/* Header Section */}
            <div className='max-w-4xl mx-auto px-6 py-8'>

                <div className='mb-6 md:mb-8'>
                    <h1 className="text-2xl md:text-4xl font-bold text-gray-900 mb-4">Your Fitness Plan</h1>

                    <button
                        className="w-full md:w-auto bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-medium shadow-md"
                        onClick={generatePlan}
                        disabled={loading}>
                        {loading ? 'Generating Plan...' : 'Generate New Plan'}
                    </button>
                </div>

                {/* Error Section */}
                {error && (
                    <div className="mb-6">
                        <p className='text-red-600 font-medium'>Error: {error}</p>
                    </div>
                )}
                {/* Plan Content */}
                {plan && (
                    <div className="space-y-8">

                        {/* Tabs container  */}
                        {plan && (
                            <div className='flex space-x-2 mb-6'>
                                <TabButton
                                    tabId="overview"
                                    label="Overview"
                                    isActive={activeTab === 'overview'}
                                    onClick={setActiveTab}
                                />

                                <TabButton
                                    tabId="workout"
                                    label="Workout Plan"
                                    isActive={activeTab === 'workout'}
                                    onClick={setActiveTab}
                                />

                                <TabButton
                                    tabId="meal"
                                    label="Meal Plan"
                                    isActive={activeTab === 'meal'}
                                    onClick={setActiveTab}
                                />
                            </div>
                        )}

                        {/* Errors */}
                        {error && (
                            <div className="mb-6">
                                <p className="text-red-600 font-medium">Error: {error}</p>
                            </div>
                        )}

                        {/* Conditional Rendering based on tab */}
                        {plan.detail && (                            <div>No plan yet, click "Generate New Plan" to get your personalized AI-generated Fitness Plan!</div>
)}
                        {plan && (
                            <div>
                                {/* Overview Tab - Health Metrics + Tips */}
                                {activeTab === 'overview' && (
                                    <div className='space-y-6'>
                                        <HealthMetrics healthMetrics={plan.health_metrics} />

                                        {plan.tips && plan.tips.length > 0 && (
                                            <div className='bg-yellow-50 p-6 rounded-lg border border-yellow-200 '>
                                                <h3 className='text-2xl font-bold text-gray-900 mb-4'>Tips for Success</h3>
                                                <ul className='space-y-2 list-decimal'>
                                                    {plan.tips.map((tip, idx) => (
                                                        <li className="mx-5 text-gray-700" key={idx}>{tip}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        )}

                        {activeTab === 'workout' && (
                            <div>
                                <WorkoutPlan workoutPlan={plan.workout_plan} />
                                
                            </div>
                        )}
                        {activeTab === 'meal' && (
                            <div>
                                <MealPlan mealPlan={plan.meal_plan} />

                            </div>
                        )}





                    </div>
                )}
            </div>
        </div>
    )
}

export default PlanPage