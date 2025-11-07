# backend/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from backend.database.config import get_db
from backend.database.models import User
from backend.auth.security import hash_password, verify_password, create_access_token

router = APIRouter()

# request/response schemas (small local defs to avoid import problems)
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str | None = None
    role: str | None = "user"

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/register", response_model=dict)
async def register(user: RegisterRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.username == user.username)
    existing = await db.execute(stmt)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already exists")
    new = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
        role=user.role
    )
    db.add(new)
    await db.commit()
    await db.refresh(new)
    # return basic user object (tests expect code 200)
    return {"id": new.id, "username": new.username, "email": new.email}

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.username == payload.username)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "username": user.username}}
