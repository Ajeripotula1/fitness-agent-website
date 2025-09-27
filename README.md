# FitnessAgent Website

A single-page application (SPA) that provides personalized fitness and nutrition planning through an AI-powered agent. The system uses structured reasoning and scientific tools to create evidence-based workout and meal plans.

## Architecture

- **Frontend**: React with Vite (JavaScript)
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with Docker
- **AI Agent**: Strands SDK (development) → AWS Bedrock AgentCore Runtime (production)

## Project Structure

```
fitness-agent-website/
├── .kiro/specs/           # Kiro specifications
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── main.py       # FastAPI application
│   │   ├── database.py   # Database connection
│   │   ├── models/       # Database models
│   │   ├── api/          # API routes
│   │   └── tools/        # Agent tools
│   └── requirements.txt
├── frontend/              # React frontend
│   ├── src/
│   └── package.json
├── docker-compose.yml     # PostgreSQL database
└── README.md
```

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose

### 1. Database Setup
```bash
# Start PostgreSQL
docker-compose up -d postgres
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with database credentials
cp .env.example .env  # Edit with your settings

# Run FastAPI server
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Services

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Database**: localhost:5433
- **API Docs**: http://localhost:8000/docs

## Features

- User authentication and profiles
- Goal-based fitness planning
- AI-powered workout generation
- Personalized meal planning
- Conversational plan refinement
- Daily/weekly progress tracking

## Development Status

- [x] Task 1: Development environment setup
- [ ] Task 2: Database models and migrations
- [ ] Task 3: Authentication system
- [ ] Task 4: Goal input interface
- [ ] Task 5: Scientific calculation tools
- [ ] Task 6: Strands SDK agent integration
- [ ] Task 7: Plan generation and display
- [ ] Task 8: Conversational interface
- [ ] Task 9: Daily tracking interface
- [ ] Task 10: Error handling
- [ ] Task 11: Session management
- [ ] Task 12: Testing and documentation

## Contributing

1. Follow the task list in `.kiro/specs/fitness-agent-website/tasks.md`
2. Create feature branches for each task
3. Test thoroughly before committing
4. Update documentation as needed

## License

Private project - All rights reserved