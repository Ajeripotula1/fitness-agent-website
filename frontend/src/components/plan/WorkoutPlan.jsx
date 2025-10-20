const WorkoutPlan = ({ workoutPlan }) => {
    console.log("Props", workoutPlan)

    if (!workoutPlan || Object.keys(workoutPlan).length === 0) {
        return (
            <div className="text-center py-8">
                <div className="text-gray-400 text-lg">No workout plan available</div>
            </div>
        )
    }

    const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    // Helper function to get day abbreviation
    const getDayAbbrev = (day) => {
        const abbrevs = {
            monday: 'MON', tuesday: 'TUE', wednesday: 'WED', 
            thursday: 'THU', friday: 'FRI', saturday: 'SAT', sunday: 'SUN'
        }
        return abbrevs[day]
    }

    // Helper function to render exercise details
    const renderExercise = (exercise, index) => (
        <div key={index} className="bg-gray-50 rounded-lg p-4 border-l-4 border-blue-500 mb-4">
            <div className="flex justify-between items-start mb-2">
                <h4 className="text-lg font-semibold text-gray-900">{exercise.name}</h4>
                <span className="text-sm text-gray-500 bg-white px-2 py-1 rounded">
                    #{index + 1}
                </span>
            </div>
            
            {/* Exercise Stats */}
            <div className="grid grid-cols-3 gap-4 mb-3">
                <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{exercise.sets}</div>
                    <div className="text-xs text-gray-500 uppercase tracking-wide">Sets</div>
                </div>
                <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">{exercise.reps}</div>
                    <div className="text-xs text-gray-500 uppercase tracking-wide">Reps</div>
                </div>
                <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">
                        {exercise.rest_seconds ? `${exercise.rest_seconds}s` : '60s'}
                    </div>
                    <div className="text-xs text-gray-500 uppercase tracking-wide">Rest</div>
                </div>
            </div>

            {/* Exercise Notes */}
            {exercise.notes && (
                <div className="bg-white rounded p-3 border border-gray-200">
                    <div className="flex items-start space-x-2">
                        <svg className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                        </svg>
                        <p className="text-sm text-gray-700">{exercise.notes}</p>
                    </div>
                </div>
            )}
        </div>
    )

    // Helper function to render workout day
    const renderWorkoutDay = (day, dayWorkout) => {
        const isRestDay = !dayWorkout || !dayWorkout.exercises || dayWorkout.exercises.length === 0

        return (
            <div key={day} className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden mb-6">
                {/* Day Header */}
                <div className={`px-6 py-4 ${isRestDay ? 'bg-gray-100' : 'bg-gradient-to-r from-blue-500 to-blue-600'}`}>
                    <div className="flex justify-between items-center">
                        <div>
                            <div className={`text-sm font-medium ${isRestDay ? 'text-gray-500' : 'text-blue-100'} uppercase tracking-wide`}>
                                {getDayAbbrev(day)}
                            </div>
                            <h3 className={`text-xl font-bold ${isRestDay ? 'text-gray-700' : 'text-white'}`}>
                                {day.charAt(0).toUpperCase() + day.slice(1)}
                            </h3>
                        </div>
                        <div className="text-right">
                            {isRestDay ? (
                                <div className="bg-gray-200 text-gray-600 px-3 py-1 rounded-full text-sm font-medium">
                                    Rest Day
                                </div>
                            ) : (
                                <div>
                                    <div className="text-white text-sm opacity-90">
                                        {dayWorkout.workout_type}
                                    </div>
                                    <div className="text-white text-xs opacity-75">
                                        {dayWorkout.duration_minutes ? `${dayWorkout.duration_minutes} min` : '45 min'}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Day Content */}
                <div className="p-6">
                    {isRestDay ? (
                        <div className="text-center py-8">
                            <div className="text-gray-400 text-lg mb-2">🛌</div>
                            <p className="text-gray-600">Recovery day - let your muscles rest and rebuild!</p>
                            <p className="text-sm text-gray-500 mt-2">Light stretching or walking is okay</p>
                        </div>
                    ) : (
                        <div>
                            {/* Workout Summary */}
                            <div className="bg-blue-50 rounded-lg p-4 mb-6">
                                <div className="flex justify-between items-center text-sm">
                                    <span className="text-gray-600">
                                        <strong>{dayWorkout.exercises.length}</strong> exercises
                                    </span>
                                    <span className="text-gray-600">
                                        Est. <strong>{dayWorkout.duration_minutes || 45}</strong> minutes
                                    </span>
                                    <span className="text-gray-600">
                                        <strong>{dayWorkout.workout_type}</strong> focus
                                    </span>
                                </div>
                            </div>

                            {/* Exercises */}
                            {dayWorkout.exercises.map((exercise, index) => renderExercise(exercise, index))}
                        </div>
                    )}
                </div>
            </div>
        )
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-2">Weekly Workout Plan</h2>
                <p className="text-gray-600">Your personalized training program</p>
            </div>

            {/* Program Overview */}
            {workoutPlan.weekly_summary && (
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200 mb-8">
                    <div className="flex items-start space-x-3">
                        <div className="bg-blue-500 rounded-full p-2">
                            <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
                            </svg>
                        </div>
                        <div>
                            <h3 className="text-lg font-semibold text-gray-900 mb-2">Program Overview</h3>
                            <p className="text-gray-700 leading-relaxed">{workoutPlan.weekly_summary}</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Weekly Schedule */}
            <div>
                {days.map(day => {
                    const dayWorkout = workoutPlan[day]
                    return renderWorkoutDay(day, dayWorkout)
                })}
            </div>

            {/* Program Notes */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mt-8">
                <div className="flex items-start space-x-3">
                    <svg className="w-5 h-5 text-yellow-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    <div>
                        <h4 className="font-semibold text-yellow-800 mb-2">Important Reminders</h4>
                        <ul className="text-sm text-yellow-700 space-y-1">
                            <li>• Always warm up for 5-10 minutes before starting</li>
                            <li>• Focus on proper form over heavy weight</li>
                            <li>• Rest 48-72 hours between training the same muscle groups</li>
                            <li>• Stay hydrated and listen to your body</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default WorkoutPlan