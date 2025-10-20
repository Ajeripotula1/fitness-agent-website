# Standalone Fitness Agent for PRODUCTION AgentCore Runtime
# All dependencies included in this file to avoid import issues

from dotenv import load_dotenv
import os, boto3, json
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

# Load environment variables from the same directory as this file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, '.env')

# print(f"🔍 Looking for .env file at: {env_path}")
# print(f"📁 File exists: {os.path.exists(env_path)}")

# Load the .env file
load_dotenv(env_path)

# Debug: Check if variables loaded
# print(f"🔑 AWS_BEDROCK_MODEL_ID: {os.getenv('AWS_BEDROCK_MODEL_ID')}")
# print(f"🌍 AWS_DEFAULT_REGION: {os.getenv('AWS_DEFAULT_REGION')}")

# If still not found, try loading from parent directories
if not os.getenv('AWS_BEDROCK_MODEL_ID'):
    # print("⚠️ Trying parent directory...")
    parent_env = os.path.join(os.path.dirname(current_dir), '.env')
    load_dotenv(parent_env)
    # print(f"🔑 After parent load - AWS_BEDROCK_MODEL_ID: {os.getenv('AWS_BEDROCK_MODEL_ID')}")

# Final check
if not os.getenv('AWS_BEDROCK_MODEL_ID'):
    print("❌ AWS_BEDROCK_MODEL_ID still not found!")  # Keep critical error
    # print("Available AWS environment variables:")
    # for key, value in os.environ.items():
    #     if 'AWS' in key:
    #         print(f"  {key}: {value}")
# else:
    # print("✅ Environment variables loaded successfully!")

# Create AgentCore app instance
app = BedrockAgentCoreApp()

# ===== HEALTH CALCULATIONS (copied from backend/app/utils/health_calculations.py) =====

def imperial_to_metric(weight_lbs: float, height_feet: int, height_inches: float) -> dict:
    """Convert imperial measurements to metric system"""
    total_inches = (height_feet * 12) + height_inches
    height_meters = total_inches * 0.0254
    weight_kgs = weight_lbs * 0.453592
    return {"height": height_meters, "weight": weight_kgs}

@tool
def calculate_bmi(weight_lbs: float, height_feet: int, height_inches: float) -> dict:
    """Calculate Body Mass Index (BMI) and health category from imperial measurements."""
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
    """Calculate Basal Metabolic Rate (BMR) - calories burned at rest per day."""
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
    """Calculate Total Daily Energy Expenditure (TDEE) - total calories burned per day."""
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
    """Adjust TDEE based on fitness goal to create calorie deficit/surplus."""
    if goal == "lose_weight":
        return tdee * 0.8  # 20% deficit for sustainable weight loss
    elif goal == "gain_weight":
        return tdee * 1.15  # 15% surplus for lean muscle gain
    return tdee  # maintenance calories

@tool
def calculate_macros(tdee: float, goal: str, weight_lbs: float) -> dict:
    """Calculate optimal daily macronutrient breakdown for fitness goals."""
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

# ===== PROMPTS (copied from backend/app/agent/prompts.py) =====
def get_fitness_system_prompt():
    return """You are a fitness expert. Use your calculation tools (calculate_bmi, calculate_bmr, calculate_tdee, calculate_macros) to analyze user data. Provide evidence-based workout and meal recommendations."""

# def get_fitness_system_prompt():
#     return """
#     You are FitAgent, an expert fitness trainer and nutritionist with 10+ years of experience.
    
#     PERSONALITY:
#     - Encouraging and motivational
#     - Evidence-based recommendations
#     - Practical and realistic advice
#     - Supportive but honest about challenges
    
#     AVAILABLE TOOLS:
#     - calculate_bmi: Calculate BMI and health category
#     - calculate_bmr: Calculate basal metabolic rate
#     - calculate_tdee: Calculate total daily energy expenditure  
#     - calculate_macros: Calculate optimal protein/carbs/fat targets
    
#     WORKFLOW:
#     1. ALWAYS use calculation tools to get accurate user metrics
#     2. Base all recommendations on scientific calculations
#     3. Create realistic, achievable plans
#     4. Explain your reasoning clearly
#     5. Provide structured workout and meal plans
    
#     RESPONSE FORMAT:
#     Always structure responses with clear sections:
#     - Health Metrics Summary
#     - Workout Plan Recommendations  
#     - Nutrition Plan Recommendations
#     - Key Tips & Motivation
#     """

def get_plan_generation_prompt(user_profile: dict):
    """Step 1: Analysis and planning with tools"""
    return f"""
    Analyze this user's fitness profile and create a comprehensive plan using your calculation tools:
    
    USER PROFILE:
    - Age: {user_profile.get('age', 'Not provided')}
    - Weight: {user_profile.get('weight_lbs', 'Not provided')} lbs
    - Height: {user_profile.get('height_feet', 'Not provided')}'{user_profile.get('height_inches', 0)}"
    - Gender: {user_profile.get('gender', 'Not provided')}
    - Fitness Goal: {user_profile.get('fitness_goal', 'Not provided')}
    - Activity Level: {user_profile.get('activity_level', 'moderate')}
    - Workout Days/Week: {user_profile.get('workout_days_per_week', 3)}
    - Workout Duration: {user_profile.get('workout_duration_minutes', 45)} minutes
    - Available Equipment: {user_profile.get('available_equipment', [])}
    - Dietary Preferences: {user_profile.get('dietary_preferences', [])}
    
    ANALYSIS STEPS:
    1. Calculate BMI and assess health status
    2. Calculate BMR for baseline metabolism
    3. Calculate TDEE for daily calorie needs
    4. Calculate optimal macro targets (protein/carbs/fat)
    5. Design specific workout routines for their goals and equipment
    6. Create detailed meal planning recommendations
    7. Identify key success strategies and potential challenges
    
    Provide a thorough analysis with all calculations, specific workout details, meal suggestions, and practical advice. Be comprehensive - this analysis will be structured later.
    """

# def get_structure_prompt():
#     """Step 2: Structure the analysis into the required format"""
#     return """
#     Based on the comprehensive fitness analysis above, organize the information into these specific categories:
    
#     HEALTH_METRICS: Include BMI, BMR, TDEE, macro targets, and health assessments
    
#     WORKOUT_PLAN: Structure workouts using DAYS OF THE WEEK as keys:
#     - Use "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
#     - For each day, include workout_type (e.g., "Upper Body", "Lower Body", "Cardio", "Rest")
#     - List exercises with name, sets, reps, and any notes
#     - If it's a rest day, set the day to null or include a rest day structure
#     - Add a weekly_summary with overall plan description
    
#     MEAL_PLAN: Structure nutrition recommendations using DAYS OF THE WEEK as keys:
#     - Use "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
#     - For each day, include breakfast, lunch, dinner, and optional snacks
#     - For each meal, include name, calories, macros (protein_g, carbs_g, fat_g), ingredients, and preparation
#     - Include daily_totals for each day with total calories and macros
#     - Add weekly_summary and daily_targets for overall nutrition goals
    
#     TIPS: Extract 3-5 key actionable tips for success
    
#     IMPORTANT: Always use day names (monday, tuesday, etc.) not generic labels like "day_1_upper"
#     """

def get_structure_prompt():
    """Step 2: Structure the analysis into the required format"""
    return """
    CRITICAL: Format your response as a valid JSON object with EXACTLY these keys and structure:

    {
        "health_metrics": {
            "bmi": number,
            "bmr": number, 
            "tdee": number,
            "target_calories": number,
            "macro_targets": {"protein_g": number, "carbs_g": number, "fat_g": number}
        },
        "workout_plan": {
            "monday": {
                "workout_type": "string",
                "exercises": [
                    {"name": "string", "sets": number, "reps": "string", "notes": "string"}
                ],
                "duration_minutes": number
            },
            "tuesday": null,
            "wednesday": null,
            "thursday": {
                "workout_type": "string", 
                "exercises": [
                    {"name": "string", "sets": number, "reps": "string", "notes": "string"}
                ],
                "duration_minutes": number
            },
            "friday": null,
            "saturday": null,
            "sunday": null,
            "weekly_summary": "string"
        },
        "meal_plan": {
            "day_meal": {
                "breakfast": {"name": "string", "calories": number, "protein_g": number, "carbs_g": number, "fat_g": number, "ingredients": ["string"], "preparation": "string"},
                "lunch": {"name": "string", "calories": number, "protein_g": number, "carbs_g": number, "fat_g": number, "ingredients": ["string"], "preparation": "string"},
                "dinner": {"name": "string", "calories": number, "protein_g": number, "carbs_g": number, "fat_g": number, "ingredients": ["string"], "preparation": "string"},
                "snacks": [{"name": "string", "calories": number, "protein_g": number, "carbs_g": number, "fat_g": number}]
            },
            "weekly_summary": "string",
            "daily_targets": {"calories": number, "protein_g": number, "carbs_g": number, "fat_g": number}
        },
        "tips": ["string", "string", "string", "string", "string"]
    }

    RULES:
    - Use EXACT key names shown above
    - Include ALL required fields
    - Use null for rest days
    - Numbers must be actual numbers, not strings
    - Follow the exact structure - no extra nesting
    """

# ===== PROPER SCHEMAS (copied from agent_schemas.py) =====

from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Exercise(BaseModel):
    name: str
    sets: int
    reps: str
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None

class DayWorkout(BaseModel):
    workout_type: str = Field(description="e.g., 'Upper Body', 'Lower Body', 'Full Body', 'Cardio'")
    exercises: List[Exercise]
    duration_minutes: Optional[int] = None

class WorkoutPlan(BaseModel):
    monday: Optional[DayWorkout] = None
    tuesday: Optional[DayWorkout] = None
    wednesday: Optional[DayWorkout] = None
    thursday: Optional[DayWorkout] = None
    friday: Optional[DayWorkout] = None
    saturday: Optional[DayWorkout] = None
    sunday: Optional[DayWorkout] = None
    weekly_summary: Optional[str] = None

# Single Meal
class Meal(BaseModel):
    name: str
    calories: Optional[int] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    ingredients: Optional[List[str]] = None
    preparation: Optional[str] = None

# Meals + Macros for entire day (all meals)
class DayMeals(BaseModel):
    breakfast: Optional[Meal] = None
    lunch: Optional[Meal] = None
    dinner: Optional[Meal] = None
    snacks: Optional[List[Meal]] = None

# Meal Plan 
class MealPlan(BaseModel):    
    day_meal: Optional[DayMeals] = None  # (meal info for each day)
    weekly_summary: Optional[str] = None # macros for whole week
    daily_targets: Optional[Dict] = None # target for each day

class PlanGenerationResponse(BaseModel):
    health_metrics: Dict = {}
    workout_plan: WorkoutPlan = Field(default_factory=WorkoutPlan)
    meal_plan: MealPlan = Field(default_factory=MealPlan)
    tips: List[str] = []

class ChatRequest(BaseModel):
    message: str
    plan_context: Dict = {}
# ===== AGENT CLASS =====

class FitnessAgentCore:
    """AgentCore-compatible version of FitnessAgent"""
    
    def __init__(self):
        # Initialize agent with model and tools
        self.tools = [calculate_bmi, calculate_bmr, calculate_tdee, calculate_macros]
        
        # Get model ID with fallback
        self.model_id = os.getenv('AWS_BEDROCK_MODEL_ID')
        if not self.model_id:
            # Use the model ID from your .env file as fallback
            self.model_id = 'us.anthropic.claude-sonnet-4-20250514-v1:0'
            # print(f"⚠️ Using fallback model ID: {self.model_id}")
        # else:
            # print(f"✅ Using model ID from environment: {self.model_id}")

        self.model = BedrockModel(
            model_id=self.model_id,
            temperature=0.3,        # Lower = faster, more consistent
            # max_tokens=2000,        # Limit response length
            top_p=0.9              # Focus on most likely tokens
        )

        self.agent = Agent(model=self.model, tools=self.tools)
        self.system_prompt = get_fitness_system_prompt()

    def generate_fitness_plan(self, user_profile: dict) -> dict:
        """Generate comprehensive fitness plan for user"""
        try:
            # print(f"#######GENERATING PLAN FOR USER: {user_profile} #######")
            
            # Step 1: Let agent use tools to calculate and plan
            planning_prompt = get_plan_generation_prompt(user_profile)
            raw_response = self.agent(prompt=planning_prompt, system=self.system_prompt)
            
            # Step 2: Structure the response
            structure_prompt = f"""
            {get_structure_prompt()}
            
            Previous analysis:
            {raw_response}
            """
            
            structured_response = self.agent.structured_output(
                PlanGenerationResponse, 
                prompt=structure_prompt
            )
            
            return {
                "health_metrics": structured_response.health_metrics,
                "workout_plan": structured_response.workout_plan,
                "meal_plan": structured_response.meal_plan,
                "tips": structured_response.tips,
            }

        except Exception as e:
            print(f"Error generating plan: {str(e)}")
            return {
                "health_metrics": {},
                "workout_plan": {},
                "meal_plan": {},
                "tips": [],
            }

# ===== AGENTCORE ENTRY POINT =====

@app.entrypoint
def invoke(payload, context):
    """Official AgentCore entry point"""
    try:
        # Extract user profile from payload
        user_profile = payload.get("user_profile", {})
        
        # If no user_profile, try to extract from prompt (for testing)
        if not user_profile and "user_profile" in payload.get("prompt", ""):
            user_profile = payload
        
        # Generate fitness plan
        agent = FitnessAgentCore()
        result = agent.generate_fitness_plan(user_profile)
        
        # Return in AgentCore expected format
        return {
            "response": result,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "response": {"error": str(e)},
            "status": "error"
        }

# For running as AgentCore service
if __name__ == "__main__":
    app.run()