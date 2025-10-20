const MealPlan = ({ mealPlan }) => {
    console.log("Meal Plan Props: ", mealPlan)

    if (!mealPlan || Object.keys(mealPlan).length === 0) {
        return <div>No meal plan available</div>
    }

    const { day_meal, weekly_summary, daily_targets } = mealPlan

    // Helper function to render macros (reusable)
    const renderMacros = (meal) => (
        <div className=" bg-gray-50 rounded-md p-3 mt-3">
            <h4 className="font-medium text-gray-900 mb-2">Nutrition:</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm text-gray-600">
                <div>Calories: <span className="font-medium text-gray-900">{meal.calories}</span></div>
                <div>Protein: <span className="font-medium text-gray-900">{meal.protein_g}g</span></div>
                <div>Carbs: <span className="font-medium text-gray-900">{meal.carbs_g}g</span></div>
                <div>Fat: <span className="font-medium text-gray-900">{meal.fat_g}g</span></div>
            </div>
        </div>
    )

    // Helper function to render single meal
    const renderSingleMeal = (meal, index = 0) => (
        <div key={index} className="mt-4">
            <h4 className="text-base md:text-lg font-medium text-gray-900 mb-2">{meal.name}</h4>

            {/* Ingredients */}
            {meal.ingredients && (
                <div className="mb-3">
                    <h5 className="font-medium text-gray-900 mb-1">Ingredients:</h5>
                    <ul className="mx-4 text-sm text-gray-700 space-y-1 list-disc">
                        {meal.ingredients.map((ingredient, idx) => (
                            <li key={idx}>{ingredient}</li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Preparation */}
            <div className="space-y-3 md:space-y-4">

            {meal.preparation && (
                <div>
                    <h5 className="font-medium text-gray-900 mb-1">Preparation:</h5>
                    <p className="text-sm text-gray-700">{meal.preparation}</p>
                </div>
            )}

            {/* Macros */}
            {renderMacros(meal)}
        </div>
        </div>
    )

    // Main render function for each meal type
    const renderMealSection = (mealType, mealData) => {
        if (!mealData) return null

        const mealTitle = mealType.charAt(0).toUpperCase() + mealType.slice(1)

        return (
            <div key={mealType} className="bg-white rounded-lg shadow-md p-4 md:p-6 border border-gray-200">
                <h3 className="text-xl font-semibold text-gray-900">{mealTitle}</h3>

                {Array.isArray(mealData) ? (
                    // Handle snacks (array of meals)
                    <div className="space-y-4">
                        {mealData.map((snack, index) => renderSingleMeal(snack, index))}
                    </div>
                ) : (
                    // Handle regular meals (single meal object)
                    renderSingleMeal(mealData)
                )}
            </div>
        )
    }

    return (
        <div className="space-y-6 md:space-y-6">
            {/* Header */}
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Daily Meal Plan</h2>

            {/* Weekly Summary Card */}
            {weekly_summary && (
                <div className="bg-blue-50 rounded-lg border border-blue-200 p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">Overview</h3>
                    <p className="text-gray-700">{weekly_summary}</p>
                </div>
            )}

            {/* Daily Targets Card */}
            {daily_targets && (
                <div className="bg-green-50 p-6 rounded-lg border border-green-200 mb-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-3">Daily Targets</h3>
                    <div className="space-x-4">
                        <span>Calories: <span className="font-medium text-gray-900">{daily_targets.calories}</span></span>
                        <span>Protein: <span className="font-medium text-gray-900">{daily_targets.protein_g}g</span></span>
                        <span>Carbs: <span className="font-medium text-gray-900">{daily_targets.carbs_g}g</span></span>
                        <span>Fat: <span className="font-medium text-gray-900">{daily_targets.fat_g}g</span></span>
                    </div>
                </div>
            )}

            {/* Meals */}
            <div className="space-y-6">
                {day_meal && Object.entries(day_meal).map(([mealType, mealData]) =>
                    renderMealSection(mealType, mealData)
                )}
            </div>
        </div>
    )
}

export default MealPlan
