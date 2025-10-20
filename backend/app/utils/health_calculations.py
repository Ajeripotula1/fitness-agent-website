# backend/app/utils/health_calculations.py
from strands import tool

def imperial_to_metric(weight_lbs: float, height_feet: int, height_inches: float) -> dict:
    """Convert imperial measurements to metric system"""
    total_inches = (height_feet * 12) + height_inches
    height_meters = total_inches * 0.0254
    weight_kgs = weight_lbs * 0.453592
    return {"height": height_meters, "weight": weight_kgs}

@tool
def calculate_bmi(weight_lbs: float, height_feet: int, height_inches: float) -> dict:
    """
    Calculate Body Mass Index (BMI) and health category from imperial measurements.
    
    BMI is a measure of body fat based on height and weight. This function:
    - Converts imperial units (pounds, feet/inches) to metric
    - Calculates BMI using the standard formula: weight(kg) / height(m)²
    - Categorizes the result as Underweight, Normal weight, Overweight, or Obese
    
    Args:
        weight_lbs: Body weight in pounds (must be positive)
        height_feet: Height in feet (typically 3-8)
        height_inches: Additional inches for height (0-11.9)
    
    Returns:
        dict: {
            "bmi": float - BMI value rounded to 1 decimal place,
            "category": str - Health category based on BMI ranges
        }
    
    Example:
        calculate_bmi(150, 5, 8) returns {"bmi": 22.8, "category": "Normal weight"}
    """
    metric = imperial_to_metric(weight_lbs, height_feet, height_inches)
    bmi = round(metric['weight'] / (metric['height'] ** 2), 1)
    
    if bmi < 18.5:
        category = 'Underweight'
    elif bmi < 25:
        category = 'Normal weight'
    elif bmi < 30:
        category = 'Overweight'
    else:
        category = 'Obese'
    
    return {"bmi": bmi, "category": category}

@tool
def calculate_bmr(weight_lbs: float, height_feet: int, height_inches: float, age: int, gender: str) -> dict:
    """
    Calculate Basal Metabolic Rate (BMR) - calories burned at rest per day.
    
    BMR represents the minimum energy needed to maintain basic physiological functions
    like breathing, circulation, and cell production. Uses the Mifflin-St Jeor equation,
    which is considered the most accurate for most people.
    
    Formulas:
    - Men: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5
    - Women: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161
    - Other: Average of male and female formulas
    
    Args:
        weight_lbs: Body weight in pounds
        height_feet: Height in feet
        height_inches: Additional inches for height
        age: Age in years (13-120)
        gender: 'male', 'female', or 'other'
    
    Returns:
        dict: {"bmr": int - Daily calories burned at rest}
    
    Example:
        calculate_bmr(170, 5, 9, 25, 'male') returns {"bmr": 1750}
    """
    metric = imperial_to_metric(weight_lbs, height_feet, height_inches)
    
    male_bmr = (10 * metric['weight']) + (6.25 * metric['height'] * 100) - (5 * age) + 5
    female_bmr = (10 * metric['weight']) + (6.25 * metric['height'] * 100) - (5 * age) - 161
    other_bmr = (male_bmr + female_bmr) / 2
    
    if gender.lower() == 'male':
        bmr = int(male_bmr)
    elif gender.lower() == 'female':
        bmr = int(female_bmr)
    else: 
        bmr = int(other_bmr)

    return {"bmr": bmr}

@tool
def calculate_tdee(bmr: int, activity_level: str) -> dict:
    """
    Calculate Total Daily Energy Expenditure (TDEE) - total calories burned per day.
    
    TDEE accounts for all energy expenditure including BMR plus physical activity.
    Multiplies BMR by an activity factor based on exercise frequency and intensity.
    
    Activity Levels:
    - sedentary: 1.2 (little/no exercise, desk job)
    - light: 1.375 (light exercise 1-3 days/week)
    - moderate: 1.55 (moderate exercise 3-5 days/week)
    - active: 1.725 (heavy exercise 6-7 days/week)
    - very_active: 1.9 (very heavy exercise, physical job, training 2x/day)
    
    Args:
        bmr: Basal Metabolic Rate in calories per day
        activity_level: Activity level string (defaults to 'moderate' if invalid)
    
    Returns:
        dict: {"tdee": float - Total daily calories burned}
    
    Example:
        calculate_tdee(1750, 'moderate') returns {"tdee": 2712.5}
    """
    activity_multiplier = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    tdee = bmr * activity_multiplier.get(activity_level.lower(), 1.55)
    return {"tdee": tdee}

def calorie_goal(tdee: float, goal: str) -> float:
    """
    Adjust TDEE based on fitness goal to create calorie deficit/surplus.
    
    Args:
        tdee: Total Daily Energy Expenditure
        goal: 'lose_weight', 'gain_weight', or 'maintain'
    
    Returns:
        float: Adjusted daily calorie target
    """
    if goal == "lose_weight":
        return tdee * 0.8  # 20% deficit for sustainable weight loss
    elif goal == "gain_weight":
        return tdee * 1.15  # 15% surplus for lean muscle gain
    return tdee  # maintenance calories

@tool
def calculate_macros(tdee: float, goal: str, weight_lbs: float) -> dict:
    """
    Calculate optimal daily macronutrient breakdown for fitness goals.
    
    Determines protein, carbohydrate, and fat targets based on:
    - Adjusted calorie intake (deficit/surplus based on goal)
    - Body weight for protein requirements
    - Goal-specific macro ratios for optimal body composition
    
    Macro Strategies:
    - Lose Weight: Higher protein (muscle preservation), moderate fat, lower carbs
    - Gain Weight: Moderate protein, higher carbs (energy), moderate fat
    - Maintain: Balanced distribution
    
    Calorie Values:
    - Protein: 4 calories per gram
    - Carbohydrates: 4 calories per gram  
    - Fat: 9 calories per gram
    
    Args:
        tdee: Total Daily Energy Expenditure in calories
        goal: 'lose_weight', 'gain_weight', 'maintain', or 'other'
        weight_lbs: Body weight in pounds (for protein calculation)
    
    Returns:
        dict: {
            "protein_g": int - Daily protein grams,
            "carbs_g": int - Daily carbohydrate grams,
            "fat_g": int - Daily fat grams,
            "protein_calories": int - Calories from protein,
            "carbs_calories": int - Calories from carbs,
            "fat_calories": int - Calories from fat,
            "total_calories": int - Total daily calories,
            "protein_percentage": int - Percent calories from protein,
            "carb_percentage": int - Percent calories from carbs,
            "fat_percentage": int - Percent calories from fat
        }
    
    Example:
        calculate_macros(2500, 'lose_weight', 170) returns detailed macro breakdown
    """
    calories = calorie_goal(tdee, goal)

    # Goal-specific protein and fat ratios
    if goal == 'lose_weight':
        protein_per_lb = 1.1  # Higher protein preserves muscle in deficit
        fat_ratio = 0.27      # 27% of calories from fat
    elif goal == 'gain_weight':
        protein_per_lb = 0.9  # Adequate protein for muscle building
        fat_ratio = 0.25      # 25% of calories from fat
    else:  # maintain or other
        protein_per_lb = 1.0  # Standard protein intake
        fat_ratio = 0.27      # 27% of calories from fat

    # Calculate macronutrients
    protein_grams = weight_lbs * protein_per_lb
    protein_calories = protein_grams * 4

    fat_calories = calories * fat_ratio
    fat_grams = fat_calories / 9

    carbs_calories = calories - (protein_calories + fat_calories)
    carbs_grams = carbs_calories / 4

    return {
        'protein_g': round(protein_grams),
        'carbs_g': round(carbs_grams),
        'fat_g': round(fat_grams),
        'protein_calories': round(protein_calories),
        'carbs_calories': round(carbs_calories),
        'fat_calories': round(fat_calories),
        'total_calories': round(calories),
        'protein_percentage': round(protein_calories / calories * 100),
        'carb_percentage': round(carbs_calories / calories * 100),
        'fat_percentage': round(fat_calories / calories * 100)
    }
