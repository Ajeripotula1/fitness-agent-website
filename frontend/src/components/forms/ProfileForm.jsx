import { useState, useEffect } from 'react';

// Passed in from Parent: initial formData, submit functionality, submitting status
const ProfileForm = ({ onSubmit, initialData = {}, isSubmitting = false }) => {
    // User Profile state management 
    const [formData, setFormData] = useState({
        // Basic info
        age: initialData?.age || '',
        weight: initialData?.weight || '',
        height_feet: initialData?.height_feet || '',
        height_inches: initialData?.height_inches || '',
        gender: initialData?.gender || '',
        fitness_goal: initialData?.fitness_goal || '',
        
        // Activity & preferences
        activity_level: initialData?.activity_level || '',
        workout_days_per_week: initialData?.workout_days_per_week || '',
        workout_duration_minutes: initialData?.workout_duration_minutes || '',
        available_equipment: initialData?.available_equipment || [],
        dietary_preferences: initialData?.dietary_preferences || []
    });

    const [errors, setErrors] = useState({});
    const [bmi, setBmi] = useState(null);

    // Calculate BMI in real-time when user metrics change
    useEffect(() => {
        if (formData.height_feet && formData.weight) {
            const totalInches = (parseInt(formData.height_feet) * 12) + (parseFloat(formData.height_inches) || 0);
            const heightMeters = totalInches * 0.0254;
            const weightKg = parseFloat(formData.weight) * 0.453592;
            const calculatedBmi = weightKg / (heightMeters * heightMeters);
            setBmi(calculatedBmi.toFixed(1));
        } else {
            setBmi(null);
        }
    }, [formData.height_feet, formData.height_inches, formData.weight]);

    // Track input changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        // Clear errors when user is modifiying that field
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };
    
    // Track Array input changes (check boxes)
    const handleArrayChange = (field, value, checked) => {
        setFormData(prev => ({
            ...prev,
            [field]: checked // for the "field" input array
                ? [...prev[field], value] // if checked is true: Spread field arr and add that value to the arr
                : prev[field].filter(item => item !== value) // if checked is not true: filter out all values that are not value
        }));
    };

    const validateForm = () => {
        const newErrors = {};
        
        if (!formData.age || formData.age < 13 || formData.age > 120) {
            newErrors.age = 'Age must be between 13 and 120';
        }
        
        if (!formData.weight || formData.weight <= 0) {
            newErrors.weight = 'Weight must be greater than 0';
        }
        
        if (!formData.height_feet || formData.height_feet < 3 || formData.height_feet > 8) {
            newErrors.height_feet = 'Height must be between 3 and 8 feet';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        
        if (validateForm()) {
            const submitData = {
                ...formData,
                age: parseInt(formData.age),
                weight: parseFloat(formData.weight),
                height_feet: parseInt(formData.height_feet),
                height_inches: formData.height_inches ? parseFloat(formData.height_inches) : 0,
                workout_days_per_week: formData.workout_days_per_week ? parseInt(formData.workout_days_per_week) : null,
                workout_duration_minutes: formData.workout_duration_minutes ? parseInt(formData.workout_duration_minutes) : null
            };
            
            onSubmit(submitData);
        }
    };

    const getBmiCategory = (bmiValue) => {
        if (bmiValue < 18.5) return { category: 'Underweight', color: 'text-blue-600' };
        if (bmiValue < 25) return { category: 'Normal weight', color: 'text-green-600' };
        if (bmiValue < 30) return { category: 'Overweight', color: 'text-yellow-600' };
        return { category: 'Obese', color: 'text-red-600' };
    };

    const equipmentOptions = [
        'dumbbells', 'barbell', 'resistance_bands', 'pull_up_bar', 
        'kettlebells', 'treadmill', 'stationary_bike', 'yoga_mat', 'none'
    ];

    const dietaryOptions = [
        'vegetarian', 'vegan', 'gluten_free', 'dairy_free', 
        'keto', 'paleo', 'low_carb', 'none'
    ];

    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <h2 className="text-2xl font-bold text-center">Your Fitness Profile</h2>
            
            {/* BMI Preview */}
            {bmi && (
                <div className="bg-blue-50 p-4 rounded-lg border">
                    <h3 className="font-semibold mb-2">Your BMI Preview</h3>
                    <div className="flex items-center gap-4">
                        <span className="text-2xl font-bold">{bmi}</span>
                        <span className={`font-medium ${getBmiCategory(parseFloat(bmi)).color}`}>
                            {getBmiCategory(parseFloat(bmi)).category}
                        </span>
                    </div>
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
                {/* Basic Information Section */}
                <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold mb-4">Basic Information</h3>
                    
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium mb-1">Age</label>
                            <input
                                type="number"
                                name="age"
                                value={formData.age}
                                onChange={handleChange}
                                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                                placeholder="Enter your age"
                            />
                            {errors.age && <p className="text-red-500 text-sm mt-1">{errors.age}</p>}
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">Weight (lbs)</label>
                            <input
                                type="number"
                                name="weight"
                                value={formData.weight}
                                onChange={handleChange}
                                step="0.1"
                                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                                placeholder="Enter your weight"
                            />
                            {errors.weight && <p className="text-red-500 text-sm mt-1">{errors.weight}</p>}
                        </div>
                    </div>

                    <div className="mt-4">
                        <label className="block text-sm font-medium mb-1">Height</label>
                        <div className="flex gap-2">
                            <select
                                name="height_feet"
                                value={formData.height_feet}
                                onChange={handleChange}
                                className="flex-1 p-2 border rounded focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="">Feet</option>
                                {[3, 4, 5, 6, 7, 8].map(ft => (
                                    <option key={ft} value={ft}>{ft}</option>
                                ))}
                            </select>
                            <input
                                type="number"
                                name="height_inches"
                                value={formData.height_inches}
                                onChange={handleChange}
                                min="0"
                                max="11.9"
                                step="0.1"
                                className="flex-1 p-2 border rounded focus:ring-2 focus:ring-blue-500"
                                placeholder="Inches"
                            />
                        </div>
                        {errors.height_feet && <p className="text-red-500 text-sm mt-1">{errors.height_feet}</p>}
                    </div>

                    <div className="mt-4">
                        <label className="block text-sm font-medium mb-1">Gender</label>
                        <select
                            name="gender"
                            value={formData.gender}
                            onChange={handleChange}
                            className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="">Select gender</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                </div>

                {/* Goals & Activity Section */}
                <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold mb-4">Goals & Activity</h3>
                    
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium mb-1">Primary Fitness Goal</label>
                            <select
                                name="fitness_goal"
                                value={formData.fitness_goal}
                                onChange={handleChange}
                                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="">Select your goal</option>
                                <option value="lose-weight">Lose Weight</option>
                                <option value="gain-weight">Gain Weight</option>
                                <option value="maintain">Maintain Weight</option>
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">Current Activity Level</label>
                            <select
                                name="activity_level"
                                value={formData.activity_level}
                                onChange={handleChange}
                                className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                            >
                                <option value="">Select activity level</option>
                                <option value="sedentary">Sedentary (little/no exercise)</option>
                                <option value="light">Light (light exercise 1-3 days/week)</option>
                                <option value="moderate">Moderate (moderate exercise 3-5 days/week)</option>
                                <option value="active">Active (heavy exercise 6-7 days/week)</option>
                                <option value="very_active">Very Active (very heavy exercise, physical job)</option>
                            </select>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium mb-1">Workout Days per Week</label>
                                <select
                                    name="workout_days_per_week"
                                    value={formData.workout_days_per_week}
                                    onChange={handleChange}
                                    className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                                >
                                    <option value="">Select days</option>
                                    {[1, 2, 3, 4, 5, 6, 7].map(days => (
                                        <option key={days} value={days}>{days} day{days > 1 ? 's' : ''}</option>
                                    ))}
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium mb-1">Workout Duration</label>
                                <select
                                    name="workout_duration_minutes"
                                    value={formData.workout_duration_minutes}
                                    onChange={handleChange}
                                    className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500"
                                >
                                    <option value="">Select duration</option>
                                    <option value="15">15 minutes</option>
                                    <option value="30">30 minutes</option>
                                    <option value="45">45 minutes</option>
                                    <option value="60">60 minutes</option>
                                    <option value="90">90 minutes</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Equipment & Preferences Section */}
                <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="text-lg font-semibold mb-4">Equipment & Preferences</h3>
                    
                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium mb-2">Available Equipment</label>
                            <div className="grid grid-cols-2 gap-2">
                                {equipmentOptions.map(equipment => (
                                    <label key={equipment} className="flex items-center">
                                        <input 
                                            type="checkbox"
                                            checked={formData.available_equipment.includes(equipment)}
                                            onChange={(e) => handleArrayChange('available_equipment', equipment, e.target.checked)}
                                            className="mr-2"
                                        />
                                        <span className="capitalize">{equipment.replace('_', ' ')}</span>
                                    </label>
                                ))}
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-2">Dietary Preferences</label>
                            <div className="grid grid-cols-2 gap-2">
                                {dietaryOptions.map(diet => (
                                    <label key={diet} className="flex items-center">
                                        <input 
                                            type="checkbox"
                                            checked={formData.dietary_preferences.includes(diet)}
                                            onChange={(e) => handleArrayChange('dietary_preferences', diet, e.target.checked)}
                                            className="mr-2"
                                        />
                                        <span className="capitalize">{diet.replace('_', ' ')}</span>
                                    </label>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="w-full bg-blue-500 text-white py-3 px-4 rounded-lg hover:bg-blue-600 disabled:opacity-50 font-medium"
                >
                    {isSubmitting ? 'Saving Profile...' : 'Save Profile'}
                </button>
            </form>
        </div>
    );
};

export default ProfileForm;
