import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from backend.auth.security import hash_password

@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    """Test user registration"""
    response = await async_client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "pass123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    """Test user login"""
    await async_client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "pass123"
        }
    )
    
    response = await async_client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "pass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_invalid_login(async_client: AsyncClient):
    """Test login with invalid credentials"""
    response = await async_client.post(
        "/api/auth/login",
        json={
            "username": "nonexistent",
            "password": "wrong"
        }
    )
    assert response.status_code == 401
