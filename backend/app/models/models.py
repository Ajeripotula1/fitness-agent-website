# Define Database Models (structure and rules for tables)

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey
from datetime import datetime
from app.database import Base


### User Data Models ###
class User(Base):
    __tablename__ = 'users'
    # ID
    id = Column(String, primary_key = True, nullable=False)
    user_name = Column(String, nullable=False)
    # hashed password 
    password = Column(String, nullable=False)
    created = Column(DateTime, default = datetime.utcnow)

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    # user ID
    id = Column(String, primary_key = True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    age = Column(Integer)
    weight = Column(Float)  # in lb
    height_feet = Column(Integer)  # Feet 
    height_inches = Column(Float)  # Inches
    gender = Column(String)  # 'male', 'female', 
    fitness_goal = Column(String)  # 'lose-weight', 'gain-muscle', etc.
    activity_level = Column(String)  # 'sedentary', 'light', 'moderate', 'active', 'very_active'
    workout_days_per_week = Column(Integer)
    workout_duration_minutes = Column(Integer)
    available_equipment = Column(JSON)  # list of equipment
    # workout_preferences = Column(JSON)  # duration, frequency, etc.
    dietary_preferences = Column(JSON)  # list of restrictions, prefrences, allergies
    
### Fitness Plan Data Models ###
class FitnessPlan(Base):
    __tablename__ = "fitness_plans"
    
    id = Column(String, primary_key = True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    workout_plan = Column(JSON)  # complete workout plan
    meal_plan = Column(JSON)     # complete meal plan
    health_metrics = Column(JSON)
    tips = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    # last_modified = Column(DateTime, default=datetime.utcnow)
    
    # status = Column(String, default='active')  # 'active', 'archived', 'draft'
    # version = Column(Integer, default=1)
    # need to add tips
    

# class ConversationHistory(Base):
#     __tablename__ = "conversation_history"
    
#     id = Column(String, primary_key=True)
#     user_id = Column(String, ForeignKey('users.id'), nullable=False)
#     plan_id = Column(String, nullable=False)
#     message = Column(String, nullable=False)
#     response = Column(String, nullable=False)
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     plan_changes = Column(JSON)  # any plan modifications made

# class PlanChange(Base):
#     __tablename__ = "plan_changes"
    
#     id = Column(String, primary_key=True)
#     plan_id = Column(String, nullable=False)
#     change_type = Column(String)  # 'workout', 'meal', 'schedule'
#     description = Column(String)
#     before_data = Column(JSON)
#     after_data = Column(JSON)
#     reason = Column(String)
#     timestamp = Column(DateTime, default=datetime.utcnow)


