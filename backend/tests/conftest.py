# backend/tests/conftest.py
import pytest
import os
from httpx import AsyncClient

# Import the FastAPI app that tests will exercise.
# Tests import `backend.main:app` so we import the same.
try:
    from backend.main import app
except Exception:
    # fallback if tests run from repo root and import path differs
    from main import app  # noqa: E402

# Use seeded credentials which your seed script creates (adjust if different)
SEED_USERNAME = os.getenv("TEST_SEED_USERNAME", "dr_smith")
SEED_PASSWORD = os.getenv("TEST_SEED_PASSWORD", "doctor123")

@pytest.fixture
async def async_client():
    """
    Provides an httpx.AsyncClient that operates against the FastAPI app (no HTTP server).
    Yielded value is an AsyncClient instance (not an async generator).
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture
async def auth_headers(async_client: AsyncClient):
    """
    Returns headers dict containing a valid Bearer token for requests.
    Uses seeded user login to obtain token so tests don't need to create users.
    """
    # Attempt to login using seeded credentials
    resp = await async_client.post("/api/auth/login", json={
        "username": SEED_USERNAME,
        "password": SEED_PASSWORD
    })
    # If login fails, try register (some CI runs may not have seeded DB)
    if resp.status_code != 200:
        # try to register
        await async_client.post("/api/auth/register", json={
            "username": SEED_USERNAME,
            "email": f"{SEED_USERNAME}@example.test",
            "password": SEED_PASSWORD,
            "full_name": "Seed User"
        })
        resp = await async_client.post("/api/auth/login", json={
            "username": SEED_USERNAME,
            "password": SEED_PASSWORD
        })

    data = resp.json()
    token = data.get("access_token") or data.get("token") or ""
    return {"Authorization": f"Bearer {token}"}
