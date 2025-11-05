"""
main.py — FastAPI application entrypoint (robust imports + reports endpoint)

This file:
- attempts imports from backend.* first, then top-level packages
- exposes /api/reports/latest which reads mock or real reports
- safely seeds the DB at startup if seed_database is available
- mounts a static dashboard folder at /dashboard (if present)
- enables CORS from env variable CORS_ORIGINS
"""

import os
import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Configure basic logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")

# Helper: try imports from backend.* then fallback to top-level
def try_import(module_name: str, attr: str = None):
    """
    Try to import attr from module_name using two common layouts:
    - backend.<module_name>
    - <module_name>
    Return the imported object or None.
    """
    import importlib

    candidates = [f"backend.{module_name}", module_name]
    for cand in candidates:
        try:
            mod = importlib.import_module(cand)
            if attr:
                return getattr(mod, attr)
            return mod
        except Exception:
            continue
    return None

# Try to import routers and seed function
patients_router = try_import("api.patients", "router")
auth_router = try_import("api.auth", "router")
seed_database = try_import("database.seed_data", "seed_database")

# CORS origins from env (comma-separated), default to localhost dev ports
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
).split(",")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        if seed_database:
            log.info("Seeding database...")
            try:
                seed_database()
                log.info("Database seeded.")
            except Exception as e:
                log.exception("Seed database failed: %s", e)
        else:
            log.info("No seed_database() found — skipping seeding.")
    except Exception:
        log.exception("Error during startup seeding.")
    yield
    # Shutdown - add any cleanup here if needed
    log.info("Shutting down application...")

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
    allow_origins=[o.strip() for o in CORS_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers if available
if auth_router:
    try:
        app.include_router(auth_router)
        log.info("Included auth router.")
    except Exception:
        log.exception("Failed to include auth router.")
else:
    log.warning("Auth router not found; continuing without auth routes.")

if patients_router:
    try:
        app.include_router(patients_router)
        log.info("Included patients router.")
    except Exception:
        log.exception("Failed to include patients router.")
else:
    log.warning("Patients router not found; continuing without patient routes.")

# Health and root endpoints
@app.get("/")
def read_root() -> Dict[str, Any]:
    """Root endpoint with API information"""
    return {
        "message": "Medical Records API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "medical-records-api"}

# Reports endpoint - serve the latest reports from likely locations
REPORT_CANDIDATES = [
    Path("backend/reports/mock_report.json"),
    Path("backend/reports/combined_latest.json"),
    Path("reports/mock_report.json"),
    Path("reports/combined_latest.json"),
]

def find_report_path() -> Path:
    for p in REPORT_CANDIDATES:
        if p.exists():
            return p
    # fallback: any json file in backend/reports or reports
    for folder in (Path("backend/reports"), Path("reports")):
        if folder.exists():
            json_files = list(folder.glob("*.json"))
            if json_files:
                return json_files[0]
    return None

@app.get("/api/reports/latest")
def api_reports_latest() -> Dict:
    """
    Return the latest combined report JSON.
    Tries multiple candidate paths under backend/reports/ and reports/.
    """
    p = find_report_path()
    if not p:
        log.warning("No report file found in expected locations.")
        raise HTTPException(status_code=404, detail="Report not found")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data
    except Exception as e:
        log.exception("Failed reading report %s: %s", str(p), e)
        raise HTTPException(status_code=500, detail="Failed to read report")

# Optional: mount static dashboard if folder present
DASHBOARD_DIR = Path("dashboard")
if DASHBOARD_DIR.exists() and DASHBOARD_DIR.is_dir():
    app.mount("/dashboard", StaticFiles(directory=str(DASHBOARD_DIR), html=True), name="dashboard")
    log.info("Mounted dashboard static files at /dashboard")
else:
    log.info("No dashboard directory found; static mount skipped.")

# Entrypoint for module import or uvicorn invocation
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )
