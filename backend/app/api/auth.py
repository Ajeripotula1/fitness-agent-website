# Server setup and helper libraries
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import uuid
# Token extraction from request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
# handles password hashing 
from pwdlib import PasswordHash
# Data Models and DB Session
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User as UserModel
# Environment Variables
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Extract Token from request to auth/token endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Hash plaintext password 
password_hash = PasswordHash.recommended()
def hash_password(password:str):
    return password_hash.hash(password)

# Verify hashed password 
def verify_password(password:str, hashed_password:str):
    return password_hash.verify(password, hashed_password)

### Models ###
# User creation and login endpoint
class UserCreate(BaseModel):
    username: str
    password: str
# Response for creation and login
class UserCreateResponse(BaseModel):
    id: str
    username: str
    created: datetime
# JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str

### Authorization and Authentication Helper Functions ####
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Build JWT payload and encode it
    """
    to_encode = data.copy()
    # Set expiary time
    if expires_delta:
         expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiary time to data object
    to_encode.update({"exp" : expire})
    # Convert Python dict to crypotographically signed string of structure: header.payload.signature
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def authenticate_user(db, user_name:str, password:str):
    """
    Verify user credentials against DB entry
    """
    # Locate user in table 
    user = db.query(UserModel).filter(UserModel.user_name == user_name).first()
    if not user:
        return False
    
    # Verify hashed password
    if not verify_password(password, user.password):
        return False 
    
    # Return User DB Instance 
    return user 

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    """
    Extract + Verify JWT token and return current user
    """
    # Make sure we are receiving token properly
    print(f"🔍 DEBUG: Received token: {token[:50]}...")  # Show first 50 chars
    # Build Credentials Exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        # Decode JWT and get username 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"🔍 DEBUG: Decoded payload: {payload}")
        # Extract subscriber (user name) to identify user
        user_name: str = payload.get("sub")
        print(f"🔍 DEBUG: Extracted username: '{user_name}'")
        
        if user_name is None: 
            print("❌ DEBUG: user_name is None!")
            raise credentials_exception
            
    except InvalidTokenError as e:
        print(f"❌ DEBUG: Token decode error: {e}")
        raise credentials_exception
    
    # Query Database for user
    print(f"🔍 DEBUG: Querying DB for user_name: '{user_name}'")
    # Verify that the user exists in the DB
    user = db.query(UserModel).filter(UserModel.user_name == user_name).first()
    print(f"🔍 DEBUG: Found user: {user}")
    
    if user is None:
        print("❌ DEBUG: User not found in database!")
        raise credentials_exception
        
    print(f"✅ DEBUG: Successfully found user: {user.user_name}")
    return user


### API Routes ###
router = APIRouter(prefix='/auth', tags=['auth'])

@router.get('/test')
def test():
    """
        Test Endpoint 
    """
    return {'message': 'test'}

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data:UserCreate, db:Session = Depends(get_db)):
    """
    Register a new user by verifying and storing information 
    """
    # Check if user exists
    user = db.query(UserModel).filter(UserModel.user_name == user_data.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail="Username already taken. Please choose a different username.")
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    # Create the new user python object
    new_user = UserModel(
        id=str(uuid.uuid4()),
        user_name=user_data.username,
        password=hashed_password,
        created=datetime.utcnow()
    )
    # save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Issue access token right way to auto login user
    
    # Create token expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Create JWT token
    access_token = create_access_token(
        data={"sub": new_user.user_name},
        expires_delta=access_token_expires
    )
    print(f"🔍 DEBUG: Created token with sub: '{new_user.user_name}'")
    print(f"🔍 DEBUG: Token starts with: {access_token[:50]}...")
    # On successful login, issue an Access Token
    return Token(access_token=access_token, token_type='bearer')

    # return UserCreateResponse(
    #     id=new_user.id,
    #     username=new_user.user_name,
    #     created=new_user.created
    # )

@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
def login(form_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    """
    Allow user to Login w/ Form, issue a JWT token
    """
    print(f"🔍 DEBUG: Login attempt for username: '{form_data.username}'")
    
    # Authenticate User 
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        print(f"❌ DEBUG: Authentication failed for: '{form_data.username}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"✅ DEBUG: Authentication successful for: '{user.user_name}'")
    
    # Create token expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Create JWT token
    access_token = create_access_token(
        data={"sub": user.user_name},
        expires_delta=access_token_expires
    )
    print(f"🔍 DEBUG: Created token with sub: '{user.user_name}'")
    print(f"🔍 DEBUG: Token starts with: {access_token[:50]}...")
    # On successful login, issue an Access Token
    return Token(access_token=access_token, token_type='bearer')

@router.get("/me", response_model=UserCreateResponse)
def get_me(current_user:UserModel = Depends(get_current_user)):
    """
    Get current user info - requires authentication
    """
    return UserCreateResponse(
        id=current_user.id,
        username=current_user.user_name,
        created=current_user.created
    )

