from fastapi import APIRouter
from pydantic import BaseModel, validator
from typing import Literal
from app.utils.health_calculations import calculate_bmi, calculate_bmr, calculate_tdee, calculate_macros

### Tool Models ###
class BMIRequest(BaseModel):
    weight_lbs: float
    height_feet: int
    height_inches: float

class BMIResponse(BaseModel):
    bmi: float
    category: str

class BMRRequest(BaseModel):
    weight_lbs: float
    height_feet: int
    height_inches: float
    age: int
    
    gender: str
    @validator('gender')
    def validate_gender(cls, v):
        if v.lower() not in ['male', 'female', 'other']:
            raise ValueError('Gender must be male, female, or other')
        return v.lower()

class BMRResponse(BaseModel):
    bmr: int

class TDEERequest(BaseModel):
    bmr : int
    activity_level: Literal["sedentary", "light", "moderate", "active", "very_active"]

class TDEEResponse(BaseModel):
    tdee: float

class MacrosRequest(BaseModel):
    tdee: float
    goal: Literal['lose_weight',  'gain_weight', 'maintain', 'other']
    weight_lbs: float

class MacrosResponse(BaseModel):
    protein: float
    carbs: float
    fat: float
    protein_calories: float
    carbs_calories: float
    fat_calories: float
    total_calories: float
    protein_percentage : float
    carb_percentage : float
    fat_percentage : float


### Routes ###
router = APIRouter(prefix='/tools', tags=['tools'])

@router.post('/bmi', response_model=BMIResponse)
def bmi_endpoint(request:BMIRequest):
    result = calculate_bmi(request.weight_lbs, request.height_feet, request.height_inches)
    return BMIResponse(**result)

@router.post('/bmr', response_model=BMRResponse)
def bmr_endpoint(request:BMRRequest):
    result = calculate_bmr (
                request.weight_lbs, 
                request.height_feet, 
                request.height_inches,
                request.age,
                request.gender
        )
    return (BMRResponse(**result))

@router.post('/tdee', response_model=TDEEResponse)
def tdee_endpoint(request: TDEERequest):
    result = calculate_tdee(request.bmr, request.activity_level)
    return TDEEResponse(**result)  

@router.post('/macros', response_model=MacrosResponse)
def macros_endpoint(request: MacrosRequest):
    result = calculate_macros(request.tdee, request.goal, request.weight_lbs)
    return MacrosResponse(
        protein=result['protein_g'],
        carbs=result['carbs_g'], 
        fat=result['fat_g'],
        **{k: v for k, v in result.items() if k.endswith('_calories') or k.endswith('_percentage') or k == 'total_calories'}
    )
