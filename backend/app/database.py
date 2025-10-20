from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

#  Try to load secrets from AWS first
try:
    from app.utils.secrets import load_secrets_to_env
    secrets_loaded = load_secrets_to_env()
except Exception as e:
    print(f"Could not load secrets module: {e}")
    secrets_loaded = False

# If not in AWS or secrets failed, load from .env file
if not secrets_loaded:
    load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables or secrets")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()