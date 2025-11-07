# backend/main.py
import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from backend.api.patients import router as patients_router
from backend.api.auth import router as auth_router

import uvicorn
import logging

logger = logging.getLogger(__name__)

# CORS origins from env
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Try to seed database if available
    try:
        from backend.database.seed_data import seed_database
        await seed_database()
    except Exception as e:
        logger.debug(f"Database seeding skipped or failed: {e}")
    
    yield
    # Shutdown

# Create FastAPI application
app = FastAPI(
    title="Medical Records API",
    description="Secure medical records management system with DevSecOps integration",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(patients_router, prefix="/api/patients", tags=["patients"])

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Medical Records API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "medical-records-api"}

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
