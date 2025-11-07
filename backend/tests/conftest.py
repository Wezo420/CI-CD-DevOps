import os
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient

# Set test database URL FIRST
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Import app FIRST - this ensures proper import order
from backend.main import app

# Then import database config
from backend.database.config import engine, Base

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def initialize_db():
    """Initialize test database before any tests run."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
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
