from app.utils.health_calculations import calculate_bmi, calculate_bmr, calculate_tdee, calculate_macros

def get_agent_tools():
    return [calculate_bmi, calculate_bmr, calculate_tdee, calculate_macros]
