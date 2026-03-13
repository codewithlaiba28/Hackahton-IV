"""
Authentication router for Phase 3.
Handles user registration and login.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime
import secrets
import hashlib

from app.database import get_db
from app.models.user import User, UserTier
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    user_id: str
    api_key: str
    tier: str
    name: str


def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Hash password with salt using SHA-256."""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
    return hashed, salt


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.
    
    - **email**: User's email address
    - **password**: User's password (will be hashed)
    - **name**: User's display name
    
    Returns user_id, api_key, tier, and name.
    """
    # Check if user already exists
    result = await db.execute(
        select(User).where(User.email == request.email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password, salt = hash_password(request.password)
    
    # Generate API key
    api_key = f"sk_{secrets.token_hex(32)}"
    
    # Create new user
    new_user = User(
        email=request.email,
        name=request.name,
        hashed_password=hashed_password,
        password_salt=salt,
        api_key=api_key,
        tier=UserTier.FREE,
        created_at=datetime.utcnow(),
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return AuthResponse(
        user_id=str(new_user.id),
        api_key=new_user.api_key,
        tier=str(new_user.tier),
        name=new_user.name,
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Login with email and password.
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns user_id, api_key, tier, and name if successful.
    Raises 401 if credentials are invalid.
    """
    # Find user by email
    result = await db.execute(
        select(User).where(User.email == request.email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    hashed_password, _ = hash_password(request.password, user.password_salt)
    
    if hashed_password != user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return AuthResponse(
        user_id=str(user.id),
        api_key=user.api_key,
        tier=str(user.tier),
        name=user.name,
    )
