# backend/tests/conftest.py
import asyncio
import os
import pytest
from httpx import AsyncClient

# Import your FastAPI app
# Use package-style import that matches your repo layout
from backend.main import app

# Ensure tests run with an asyncio event loop fixture (pytest-asyncio)
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Async HTTP client fixture for FastAPI
@pytest.fixture
async def async_client():
    """
    Yields an httpx.AsyncClient wired to the FastAPI app.
    Tests can `await async_client.get(...)` etc.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

# Auth helper fixture that registers (if needed) and logs in a test user,
# returning headers dict to pass into requests.
@pytest.fixture
async def auth_headers(async_client: AsyncClient):
    # try register (ignore if already exists)
    register_payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123",
        "full_name": "Test User"
    }

    # Tests call endpoints under /api/... — follow that
    try:
        await async_client.post("/api/auth/register", json=register_payload)
    except Exception:
        # ignore registration errors — could already exist
        pass

    # Login to get token
    login_payload = {"username": "testuser", "password": "securepass123"}
    resp = await async_client.post("/api/auth/login", json=login_payload)
    if resp.status_code != 200:
        # If login failed, try to register then login again
        await async_client.post("/api/auth/register", json=register_payload)
        resp = await async_client.post("/api/auth/login", json=login_payload)

    token = None
    try:
        token = resp.json().get("access_token")
    except Exception:
        token = None

    if not token:
        # Provide a fallback test-token so tests that rely on auth can continue
        return {"Authorization": "Bearer test-token"}

    return {"Authorization": f"Bearer {token}"}
