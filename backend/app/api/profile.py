from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

import uuid
from typing import Optional, List
from app.api.auth import get_current_user
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.models import User, UserProfile

### Models ### 

class ProfileCreate(BaseModel): # creating/updating a profile
    age: Optional[int] = Field(None, ge=13, le=120)
    weight: Optional[float] = Field(None, gt=0, le=1000)
    height_feet: Optional[int] = Field(None, ge=3, le=8)
    height_inches: Optional[float] = Field(None, ge=0, lt=12)
    gender: Optional[str] = None
    fitness_goal: Optional[str] = None
    # New fields
    activity_level: Optional[str] = None
    workout_days_per_week: Optional[int] = Field(None, ge=1, le=7)
    workout_duration_minutes: Optional[int] = Field(None, ge=15, le=180)
    available_equipment: Optional[List[str]] = []
    dietary_preferences: Optional[List[str]] = []


class ProfileResponse(BaseModel):
    id: str
    user_id: str
    age: Optional[int] = None
    weight: Optional[float] = None
    height_feet: Optional[int] = None
    height_inches: Optional[float] = None
    gender: Optional[str] = None
    fitness_goal: Optional[str] = None
    # New fields
    activity_level: Optional[str] = None
    workout_days_per_week: Optional[int] = None
    workout_duration_minutes: Optional[int] = None
    available_equipment: Optional[List[str]] = None
    dietary_preferences: Optional[List[str]] = None

### Routes ### 
router = APIRouter(prefix='/profile', tags=['profile'])

@router.post('/', response_model=ProfileResponse)
def create_or_update_profile(profile_data:ProfileCreate, current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    """
    Add new entry to UserProfile DB or update Existing UserProfile entry
    """
    # Check if UserProfile already exisits
    existing_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    # if user exists, update the profile
    if existing_profile:
        existing_profile.age = profile_data.age
        existing_profile.weight = profile_data.weight
        existing_profile.height_feet = profile_data.height_feet
        existing_profile.height_inches = profile_data.height_inches
        existing_profile.gender = profile_data.gender
        existing_profile.fitness_goal = profile_data.fitness_goal
        existing_profile.activity_level = profile_data.activity_level
        existing_profile.workout_days_per_week = profile_data.workout_days_per_week
        existing_profile.workout_duration_minutes = profile_data.workout_duration_minutes
        existing_profile.available_equipment = profile_data.available_equipment
        existing_profile.dietary_preferences = profile_data.dietary_preferences

        # commit changes
        db.commit()
        db.refresh(existing_profile)
        return existing_profile
    else:

        # if new user
        new_profile = UserProfile(
            id = str(uuid.uuid4()),
            user_id = current_user.id,
            age = profile_data.age,
            weight = profile_data.weight,
            height_feet = profile_data.height_feet,
            height_inches = profile_data.height_inches,
            gender = profile_data.gender,
            fitness_goal = profile_data.fitness_goal,
            activity_level=profile_data.activity_level,
            workout_days_per_week=profile_data.workout_days_per_week,
            workout_duration_minutes=profile_data.workout_duration_minutes,
            available_equipment=profile_data.available_equipment,
            dietary_preferences=profile_data.dietary_preferences
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile

@router.get("/",response_model=ProfileResponse)
def get_user_profile(current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    """
    Return the UserProfile of the currentUser
    """
    user_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if user_profile:
        return user_profile
    raise HTTPException(status_code=404, detail="Profile not found.")

