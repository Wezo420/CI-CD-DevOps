# backend/tests/conftest.py
import os
import pathlib
import pytest
import pytest_asyncio
from httpx import AsyncClient
import asyncio
from backend.database.config import init_db

# ensure DB tables exist before tests
asyncio.run(init_db())

# Ensure we import the app from backend package (CI runs pytest from backend/ with PYTHONPATH set)
try:
    from backend.main import app
except Exception:
    # fallback for local runs from repo root
    from main import app  # noqa: E402

# marker so we can see in runner logs that this conftest file was used
try:
    pathlib.Path("/tmp/backend_conftest_loaded").write_text("ok")
except Exception:
    pass

SEED_USERNAME = os.getenv("TEST_SEED_USERNAME", "dr_smith")
SEED_PASSWORD = os.getenv("TEST_SEED_PASSWORD", "doctor123")


@pytest_asyncio.fixture
async def async_client():
    """
    AsyncClient fixture that yields a real httpx.AsyncClient (has .get/.post).
    Use pytest-asyncio to ensure proper coroutine handling.
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest_asyncio.fixture
async def auth_headers(async_client: AsyncClient):
    """
    Returns headers with a valid Bearer token.
    Tries login, otherwise registers then logs in.
    """
    # try login
    resp = await async_client.post("/api/auth/login", json={
        "username": SEED_USERNAME,
        "password": SEED_PASSWORD
    })

    if resp.status_code != 200:
        # attempt to register
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

    data = {}
    try:
        data = resp.json() if resp.content else {}
    except Exception:
        data = {}

    token = data.get("access_token") or data.get("token") or ""
    return {"Authorization": f"Bearer {token}"}
