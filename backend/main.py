from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import os
from datetime import datetime
import logging

# Import routers
from api.auth import router as auth_router
from api.patients import router as patients_router
from api.security_scans import router as security_router
from database.config import init_db
from auth.security import verify_jwt_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up FastAPI server")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down FastAPI server")

app = FastAPI(
    title="Medical Records Security API",
    description="FastAPI backend for medical records with integrated DevSecOps",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(patients_router, prefix="/api/patients", tags=["patients"])
app.include_router(security_router, prefix="/api/security", tags=["security"])

@app.get("/")
async def root():
    return {
        "message": "Medical Records API with DevSecOps",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
