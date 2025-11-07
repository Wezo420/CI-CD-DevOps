# backend/auth/security.py
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext

PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET = os.getenv("JWT_SECRET", "dev-secret-for-tests")
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 60

def hash_password(plain: str) -> str:
    if len(plain) > 72:
        plain = plain[:72]
    return PWD_CTX.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return PWD_CTX.verify(plain, hashed)

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
