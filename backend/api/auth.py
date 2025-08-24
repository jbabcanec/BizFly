from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from models import get_db, User
from schemas.auth import LoginRequest, LoginResponse, UserResponse
from core.config import settings

router = APIRouter()
security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hardcoded users for now
USERS = {
    "floj": {"password": "7428", "id": "user_floj"},
    "drew": {"password": "philip", "id": "user_drew"}
}

def verify_password(plain_password: str, username: str) -> bool:
    """Verify password for hardcoded users"""
    user_data = USERS.get(username)
    if not user_data:
        return False
    return user_data["password"] == plain_password

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    if username not in USERS:
        raise credentials_exception
    return username

@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    username = login_request.username
    password = login_request.password
    
    if not verify_password(password, username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(hours=settings.jwt_expiration_hours)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    
    user_data = USERS[username]
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user_data["id"],
        username=username
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: str = Depends(get_current_user)):
    """Get current user information"""
    user_data = USERS[current_user]
    return UserResponse(
        id=user_data["id"],
        username=current_user,
        is_active=True,
        created_at=datetime.utcnow(),
        last_login=datetime.utcnow()
    )