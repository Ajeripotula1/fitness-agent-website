#### LOCAL Strands Implementation for Dev ####

from dotenv import load_dotenv
import os, boto3, json
from strands import Agent
from strands.models.bedrock import BedrockModel # BedRock: fully managed services that offers high performing FMs from leading AI companies via unified API
from app.agent.tools import get_agent_tools
from app.agent.prompts import get_fitness_system_prompt, get_plan_generation_prompt, get_structure_prompt
from app.schemas.agent_schemas import PlanGenerationResponse

load_dotenv()  # load AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

class FitnessAgent:
    def __init__(self):
        # initalize agent w/ model and optional tools
        self.tools = get_agent_tools() 
        self.model_id = os.environ['AWS_BEDROCK_MODEL_ID']
        self.model = BedrockModel(model_id=self.model_id)
        self.agent = Agent(model=self.model, tools=self.tools)
        self.system_prompt = get_fitness_system_prompt()


    def test_bedrock():
        """
        Ensure agent is connected to BedRock 
        """
        client = boto3.client('bedrock', region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'))
        resp = client.list_foundation_models()
        for fm in resp.get("modelSummaries", []):
            print(fm.get("modelName"), fm.get("modelArn"))  
    
    def test_agent(self):
        prompt = "What is the best way to learn AWS?"
        return self.agent(prompt=prompt)

    def generate_fitness_plan(self, user_profile: dict) -> dict:
        """Generate comprehensive fitness plan for user"""
        try:
            print(f"#######GENERATING PLAN FOR USER: {user_profile} #######")
            
            # Step 1: Let agent use tools to calculate and plan (tools available)
            planning_prompt = get_plan_generation_prompt(user_profile)
            raw_response = self.agent(prompt=planning_prompt, system=self.system_prompt)
            
            # Step 2: Structure the response (only PlanGenerationResponse tool available)
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
    
    # def chat(self, message: str, context: dict = None) -> str:
    #      """Chat with agent about plans"""
    #     # YOUR TASK: Handle conversational interactions
    #     pass
    
