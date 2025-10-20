# FitAgent - AI-Powered Fitness & Nutrition Planner

> **AWS AI Agent Hackathon Submission** 🏆  
> *Personalized fitness and nutrition planning powered by AWS Bedrock AgentCore*

## 🎯 What is FitAgent?

FitAgent is an intelligent fitness and nutrition planning application that leverages AWS Bedrock's AgentCore to create personalized workout routines and meal plans. The AI agent analyzes user profiles, fitness goals, and preferences to generate evidence-based recommendations using scientific calculations and health metrics.

### Current Features ✅
- **User Authentication & Profiles** - Secure user registration and login
- **Comprehensive Health Assessment** - BMI, BMR, and calorie needs calculation
- **AI-Powered Workout Generation** - Personalized routines based on goals and equipment
- **Smart Meal Planning** - Nutrition plans aligned with dietary preferences and calorie targets
- **Real-time Plan Generation** - Instant AI responses using AWS Bedrock Claude models
- **Cloud Database Integration** - AWS RDS PostgreSQL for scalable data storage

### Who Is This For? 👥
- **Fitness Enthusiasts** seeking personalized workout plans
- **Health-Conscious Individuals** wanting structured nutrition guidance  
- **Busy Professionals** needing efficient, AI-generated fitness solutions
- **Personal Trainers** looking for AI-assisted client planning tools
- **Anyone** starting their fitness journey with scientific backing

## 🏗️ Architecture & Tech Stack

### Frontend
- **React 18** with component-based architecture, tailwind styling, and responsive design

### Backend
- **FastAPI** Python REST API
- **SQLAlchemy ORM** for database operations
- **JWT Authentication** for secure user sessions
- **AWS Bedrock AgentCore Integration** for AI agent functionality

### Database & Infrastructure
- **AWS RDS PostgreSQL** for production data storage
- **Docker** for local development environment
- **AWS Bedrock** for AI model access (Claude 3 Sonnet)
- **AgentCore Runtime** for agent orchestration

### AI Agent Capabilities
- **Health Calculations** - BMI, BMR, calorie needs
- **Workout Generation** - Equipment-based routine creation
- **Meal Planning** - Macro-balanced nutrition plans
- **Scientific Reasoning** - Evidence-based recommendations

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11+
- Node.js 18+
- AWS Account with Bedrock access
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fit-agent.git
cd fit-agent
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your AWS credentials and database URL
```

### 3. Database Setup
```bash
# For local development with Docker
docker-compose up -d postgres

# Or configure your AWS RDS connection in .env
# DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/dbname
```

### 4. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your backend API URL

# Start development server
npm run dev
```

### 5. Start the Application
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend  
cd frontend
npm run dev
```

### 6. Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Environment Configuration

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# FastAPI
SECRET_KEY=your-secret-key-here
DEBUG=True

# AWS Bedrock AgentCore
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=us-east-1
AGENTCORE_AGENT_ARN=your-agent-arn
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
```

## 🔧 Development Workflow

### Project Structure
```
fit-agent/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── database.py     # Database connection
│   │   ├── models/         # SQLAlchemy models
│   │   ├── api/            # API route handlers
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── tools/          # Agent calculation tools
│   │   └── agent/          # AgentCore integration
│   ├── requirements.txt    # Python dependencies
│   └── .env.example       # Environment template
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── package.json       # Node dependencies
│   └── .env.example       # Environment template
├── docker-compose.yml     # Local PostgreSQL
└── README.md             # This file
```

### Key API Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication  
- `GET /profile` - Get user profile
- `PUT /profile` - Update user profile
- `POST /agent/generate-plan` - Generate fitness plan
- `GET /health` - Health check

## 🧪 Testing the AI Agent

### Sample User Profile
```json
{
  "age": 28,
  "weight": 70,
  "height_feet": 5,
  "height_inches": 8,
  "gender": "male",
  "fitness_goal": "lose-weight",
  "activity_level": "moderate",
  "workout_days_per_week": 4,
  "workout_duration_minutes": 45,
  "available_equipment": ["dumbbells", "resistance_bands"],
  "dietary_preferences": ["vegetarian"]
}
```

### Expected AI Response
The agent will generate:
- **Health Metrics**: BMI, BMR, daily calorie needs
- **Workout Plan**: 4-day routine with dumbbell exercises
- **Meal Plan**: Vegetarian meals meeting calorie targets
- **Tips**: Personalized advice for weight loss goals

## 🚀 Production Deployment

### AWS Infrastructure
- **AWS RDS PostgreSQL** for database
- **AWS Bedrock** for AI model access
- **AgentCore Runtime** for agent orchestration
- **EC2/ECS** for backend hosting (recommended)
- **S3 + CloudFront** for frontend hosting

### Environment Variables (Production)
Set these in your production environment:
- `DATABASE_URL` - RDS connection string
- `SECRET_KEY` - Strong secret for JWT tokens
- `DEBUG=False` - Disable debug mode
- AWS credentials via IAM roles (preferred) or environment variables

## 🎯 Hackathon Highlights

### AWS Services Used
- **AWS Bedrock** - Claude 3 Sonnet for AI reasoning
- **AgentCore Runtime** - Agent orchestration and management
- **AWS RDS** - Managed PostgreSQL database
- **IAM** - Secure credential management

### Innovation Points
- **Scientific Accuracy** - Evidence-based health calculations
- **Personalization** - Tailored plans based on individual profiles
- **Real-time AI** - Instant plan generation using Bedrock
- **Scalable Architecture** - Cloud-native design for growth
- **User Experience** - Intuitive interface for complex AI interactions

