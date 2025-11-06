import pytest
import asyncio
from httpx import AsyncClient
from backend.database.config import engine, async_session, Base
from backend.database.models import User
from auth.security import hash_password, create_access_token
from main import app

@pytest.fixture
async def setup_db():
    """Setup test database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def async_client(setup_db):
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def auth_headers(setup_db):
    """Create authenticated headers for tests"""
    async with async_session() as session:
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=hash_password("password"),
            role="user"
        )
        session.add(user)
        await session.commit()
        
        token = create_access_token({"sub": user.username, "user_id": user.id})
        return {"Authorization": f"Bearer {token}"}
