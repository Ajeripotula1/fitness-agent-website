# backend/app/api/agent.py (create new file)
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.agent_schemas import PlanGenerationResponse, ChatRequest
from app.agent.fitness_agent import FitnessAgent as FitnessAgent
from app.api.auth import get_current_user
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import UserProfile, FitnessPlan
import uuid
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from app.schemas.agent_schemas import WorkoutPlan, MealPlan
import boto3
import json
import os

router = APIRouter(prefix="/agent", tags=["agent"])

### Routes ###
@router.get("/get-plan", response_model=PlanGenerationResponse)
def get_plan(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Fetches the user Plan (if it exists) from database
    """
    try:
        # 1. Query user's plan
        plan = db.query(FitnessPlan).filter(FitnessPlan.user_id == current_user.id).first()
        
        if not plan:  # ✅ Check the correct variable
            raise HTTPException(
                status_code=404, 
                detail="No plan exists for this user"
            )
        
        # 2. Convert database JSON back to Pydantic response
        # Import your Pydantic models at the top
        from app.schemas.agent_schemas import WorkoutPlan, MealPlan
        
        db_plan = PlanGenerationResponse(
            health_metrics=plan.health_metrics,  # ✅ Already dict
            workout_plan=WorkoutPlan(**plan.workout_plan),  # ✅ Convert dict to Pydantic
            meal_plan=MealPlan(**plan.meal_plan),           # ✅ Convert dict to Pydantic  
            tips=plan.tips,  # ✅ Already list
        )
        return db_plan

    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
        
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error while fetching plan: {str(e)}"
        )

@router.get("/generate-plan", response_model=PlanGenerationResponse)
def generate_plan(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Generate personalized fitness plan using AI agent and save to DB"""
    try:
        # Get user profile
        user_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
        if not user_profile:
            raise HTTPException(status_code=404, detail="Profile not found. Please complete your profile first.")

        # Convert SQLAlchemy object to dict for agent
        profile_dict = {
            "age": user_profile.age,
            "weight_lbs": user_profile.weight,
            "height_feet": user_profile.height_feet,
            "height_inches": user_profile.height_inches,
            "gender": user_profile.gender,
            "fitness_goal": user_profile.fitness_goal,
            "activity_level": getattr(user_profile, 'activity_level', 'moderate'),
            "workout_days_per_week": getattr(user_profile, 'workout_days_per_week', 3),
            "workout_duration_minutes": getattr(user_profile, 'workout_duration_minutes', 45),
            "available_equipment": getattr(user_profile, 'available_equipment', []),
            "dietary_preferences": getattr(user_profile, 'dietary_preferences', [])
        }
        
        # ORIGINAL STRANDS CODE (commented out)
        # fitness_agent = FitnessAgent()
        # plan = fitness_agent.generate_fitness_plan(profile_dict)
        
        # NEW AGENTCORE RUNTIME CODE
        # Initialize the Bedrock AgentCore client with increased timeout
        from botocore.config import Config
        config = Config(
            read_timeout=300,  # 5 minutes
            connect_timeout=60,  # 1 minute
            retries={'max_attempts': 3}
        )
        agent_core_client = boto3.client('bedrock-agentcore', 
                                       region_name='us-east-1',
                                       config=config)
        
        # Prepare the payload with user profile
        payload = json.dumps({"user_profile": profile_dict}).encode()
        
        # AgentCore Runtime ARN (placeholder - replace with your actual ARN)
        agent_arn = os.getenv('AGENTCORE_AGENT_ARN')
        session_id = f"fitness-session-{current_user.id}"
        
        print(f"🚀 Calling AgentCore Runtime: {agent_arn}")
        print(f"📦 Payload: {json.dumps(profile_dict, indent=2)}")
        print("⏳ This may take 2-3 minutes for comprehensive fitness plan generation...")
        
        # Invoke the agent
        response = agent_core_client.invoke_agent_runtime(
            agentRuntimeArn=agent_arn,
            runtimeSessionId=session_id,
            payload=payload
        )
        
        # Process the response based on content type
        if "text/event-stream" in response.get("contentType", ""):
            # Handle streaming response
            content = []
            for line in response["response"].iter_lines(chunk_size=10):
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        line = line[6:]
                    content.append(line)
            plan_text = "\n".join(content)
            plan = json.loads(plan_text) if plan_text.strip().startswith('{') else {"response": plan_text}
            
        elif response.get("contentType") == "application/json":
            # Handle standard JSON response
            content = []
            for chunk in response.get("response", []):
                content.append(chunk.decode('utf-8'))
            plan = json.loads(''.join(content))
            
        else:
            # Handle other response types
            plan = response
        
        print("🎉 AgentCore Response:", plan)
        
        # Extract the actual fitness plan from the response
        if isinstance(plan, dict) and 'response' in plan:
            fitness_plan_data = plan['response']
            print("✅ Extracted fitness plan data:", fitness_plan_data.keys())
        else:
            fitness_plan_data = plan
        
        # Save to DB
        plan_response = PlanGenerationResponse(**fitness_plan_data)
        # 1. Delete existing plan if any
        existing_plan = db.query(FitnessPlan).filter(
            FitnessPlan.user_id == current_user.id
        ).first()
        if existing_plan:
            db.delete(existing_plan)
        
        # 2. Save new plan
        new_plan = FitnessPlan(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            workout_plan=plan_response.workout_plan.dict(),
            meal_plan=plan_response.meal_plan.dict(),
            health_metrics=plan_response.health_metrics,
            tips=plan_response.tips,
        )
        db.add(new_plan)
        db.commit()
        
        return plan_response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Error in generate_plan: {str(e)}")  # Add this for debugging
        db.rollback()
        import traceback
        traceback.print_exc()  # Print full stack trace
        raise HTTPException(status_code=500, detail=f"Error generating plan: {str(e)}")

@router.post("/chat")
def chat_with_agent(
    request: ChatRequest,
    current_user = Depends(get_current_user)
):
    """Chat with fitness agent"""
    # YOUR TASK: Implement chat functionality
    pass

@router.post("/save-plan", response_model = PlanGenerationResponse)
def save_plan(plan: PlanGenerationResponse, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Save the "Accepted" User plan to the database
    """
    try:
        # 1. Check if user already has a plan
        exisiting_plan = db.query(FitnessPlan).filter(
            FitnessPlan.user_id == current_user.id
        ).first()

        if exisiting_plan:
            db.delete(exisiting_plan)

        # 2. create Model instance to add with 
        new_plan = FitnessPlan(
            id = str(uuid.uuid4()),
            user_id = current_user.id,
            workout_plan = plan.workout_plan.dict(),
            meal_plan = plan.meal_plan.dict(),
            health_metrics = plan.health_metrics,
            tips = plan.tips,  
        )
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)
        return plan

    except SQLAlchemyError as e:
        # Database-specific errors
        db.rollback()  # Important: rollback failed transaction
        raise HTTPException(
            status_code=500, 
            detail=f"Database error while saving plan: {str(e)}"
        )
    
    except ValidationError as e:
        # Pydantic validation errors
        raise HTTPException(
            status_code=422, 
            detail=f"Invalid plan data: {str(e)}"
        )
    
    except Exception as e:
        # Catch-all for unexpected errors
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error while saving plan: {str(e)}"
        )

    
