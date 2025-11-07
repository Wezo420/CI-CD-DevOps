import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import database models FIRST to ensure they're registered
from backend.database import models

# Then import routers
from backend.api.patients import router as patients_router
from backend.api.auth import router as auth_router

# Import seed function conditionally
try:
    from backend.database.seed_data import seed_database
    HAS_SEED_DATA = True
except ImportError:
    HAS_SEED_DATA = False
    seed_database = None

import uvicorn
import logging

logger = logging.getLogger(__name__)

# CORS origins from env
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: seed DB only if available
    if HAS_SEED_DATA and seed_database:
        try:
            if callable(seed_database):
                await seed_database()
            else:
                seed_database()
        except Exception as e:
            logger.debug(f"seed_database() failed: {e}", exc_info=True)
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
