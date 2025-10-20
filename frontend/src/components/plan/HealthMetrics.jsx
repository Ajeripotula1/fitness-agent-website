
const HealthMetrics = ({ healthMetrics }) => {
    if (!healthMetrics || Object.keys(healthMetrics).length === 0) {
        return (
            <div className="text-center py-8">
                <div className="text-gray-400 text-lg">No health metrics available</div>
            </div>
        )
    }
    console.log("HEALTH", healthMetrics)

    return (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-green-500 to-emerald-600 px-6 py-4">
                <div className="flex items-center space-x-3">
                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 4a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1V8zm8 0a1 1 0 011-1h4a1 1 0 011 1v2a1 1 0 01-1 1h-4a1 1 0 01-1-1V8zm0 4a1 1 0 011-1h4a1 1 0 011 1v2a1 1 0 01-1 1h-4a1 1 0 01-1-1v-2z" clipRule="evenodd" />
                    </svg>
                    <h3 className="text-xl font-bold text-white">Your Health Metrics</h3>
                </div>
            </div>

            <div className="p-6">
                {/* Metrics Grid */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    {/* BMI */}
                    {healthMetrics.bmi && (
                        <div className="bg-blue-50 rounded-lg p-4 text-center border border-blue-200">
                            <div className="text-2xl font-bold text-blue-600">{healthMetrics.bmi}</div>
                            <div className="text-xs text-gray-500 uppercase tracking-wide">BMI</div>
                            <div className="text-sm text-gray-600 mt-1">{healthMetrics.bmi_category}</div>
                        </div>
                    )}

                    {/* BMR */}
                    {healthMetrics.bmr && (
                        <div className="bg-green-50 rounded-lg p-4 text-center border border-green-200">
                            <div className="text-2xl font-bold text-green-600">{healthMetrics.bmr}</div>
                            <div className="text-xs text-gray-500 uppercase tracking-wide">BMR</div>
                            <div className="text-sm text-gray-600 mt-1">cal/day</div>
                        </div>
                    )}

                    {/* TDEE */}
                    {healthMetrics.tdee && (
                        <div className="bg-purple-50 rounded-lg p-4 text-center border border-purple-200">
                            <div className="text-2xl font-bold text-purple-600">{healthMetrics.tdee}</div>
                            <div className="text-xs text-gray-500 uppercase tracking-wide">TDEE</div>
                            <div className="text-sm text-gray-600 mt-1">cal/day</div>
                        </div>
                    )}

                    {/* Target Calories */}
                    {healthMetrics.target_calories && (
                        <div className="bg-orange-50 rounded-lg p-4 text-center border border-orange-200">
                            <div className="text-2xl font-bold text-orange-600">{healthMetrics.target_calories}</div>
                            <div className="text-xs text-gray-500 uppercase tracking-wide">Target</div>
                            <div className="text-sm text-gray-600 mt-1">cal/day</div>
                        </div>
                    )}
                </div>

                {/* Macro Targets */}
                {(healthMetrics.protein_target_g || healthMetrics.carbs_target_g || healthMetrics.fat_target_g) && (
                    <div className="bg-gray-50 rounded-lg p-4 mb-4">
                        <h4 className="font-semibold text-gray-900 mb-3">Daily Macro Targets</h4>
                        <div className="grid grid-cols-3 gap-4 text-center">
                            {healthMetrics.protein_target_g && (
                                <div>
                                    <div className="text-lg font-bold text-red-600">{healthMetrics.protein_target_g}g</div>
                                    <div className="text-sm text-gray-600">Protein ({healthMetrics.protein_percentage}%)</div>
                                </div>
                            )}
                            {healthMetrics.carbs_target_g && (
                                <div>
                                    <div className="text-lg font-bold text-yellow-600">{healthMetrics.carbs_target_g}g</div>
                                    <div className="text-sm text-gray-600">Carbs ({healthMetrics.carbs_percentage}%)</div>
                                </div>
                            )}
                            {healthMetrics.fat_target_g && (
                                <div>
                                    <div className="text-lg font-bold text-blue-600">{healthMetrics.fat_target_g}g</div>
                                    <div className="text-sm text-gray-600">Fat ({healthMetrics.fat_percentage}%)</div>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* Health Status */}
                {healthMetrics.health_status && (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                        <div className="flex items-start space-x-3">
                            <svg className="w-5 h-5 text-yellow-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                            </svg>
                            <div>
                                <h4 className="font-semibold text-yellow-800 mb-1">Health Assessment</h4>
                                <p className="text-sm text-yellow-700">{healthMetrics.health_status}</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default HealthMetrics;
