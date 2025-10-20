import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
from app.models.models import User, UserProfile, FitnessPlan

def create_tables():
    try:
        print("Creating tables in RDS...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        print("Created tables: users, user_profiles, fitness_plans")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
