from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.tools import router as tools_router
from app.api.agent import router as agent_router
# Load environment variables
load_dotenv()

app = FastAPI(title="Fitness Agent API", version="1.0.0")
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(tools_router)
app.include_router(agent_router)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root(): 
    return {"message": "Welcome to FitAgent API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}