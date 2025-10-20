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