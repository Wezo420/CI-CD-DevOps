# backend/auth/security.py
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
import bcrypt  # ADD THIS IMPORT

# REMOVE THIS LINE: PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET = os.getenv("JWT_SECRET", "dev-secret-for-tests")
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 60

def hash_password(plain: str) -> str:
    # Use bcrypt directly with proper byte handling
    password_bytes = plain.encode('utf-8')
    # Bcrypt has a 72-byte limit - truncate if needed
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    # Hash using bcrypt directly
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    # Use bcrypt directly with proper byte handling
    password_bytes = plain.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return token

def verify_jwt_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
