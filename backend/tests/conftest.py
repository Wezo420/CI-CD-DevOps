import os
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient

# Set test database URL FIRST
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Import database config FIRST
from backend.database.config import engine, Base

# Import models to ensure they're registered with Base
from backend.database import models

# Then import app
from backend.main import app

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_db():
    """Initialize test database before any tests run."""
    # NUCLEAR OPTION: Use a completely fresh approach
    import sqlite3
    
    # Close all connections first
    await engine.dispose()
    
    # Delete any existing test database
    if os.path.exists("./test.db"):
        os.remove("./test.db")
    
    # Create fresh database with SQLite directly
    conn = sqlite3.connect('./test.db')
    conn.close()
    
    # Now let SQLAlchemy handle the schema
    async with engine.begin() as conn:
        # Drop everything forcefully
        await conn.run_sync(lambda sync_conn: Base.metadata.drop_all(sync_conn, checkfirst=False))
        # Create everything fresh
        await conn.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, checkfirst=False))
    
    yield

@pytest_asyncio.fixture
async def async_client():
    """AsyncClient fixture for testing."""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

@pytest_asyncio.fixture
async def auth_headers(async_client: AsyncClient):
    """Returns headers with a valid Bearer token."""
    SEED_USERNAME = "dr_smith"
    SEED_PASSWORD = "doctor123"
    
    # Try to register first
    await async_client.post("/api/auth/register", json={
        "username": SEED_USERNAME,
        "email": f"{SEED_USERNAME}@example.test",
        "password": SEED_PASSWORD,
        "full_name": "Seed User"
    })
    
    # Then login
    resp = await async_client.post("/api/auth/login", json={
        "username": SEED_USERNAME,
        "password": SEED_PASSWORD
    })
    
    data = resp.json()
    token = data.get("access_token") or data.get("token") or ""
    return {"Authorization": f"Bearer {token}"}
