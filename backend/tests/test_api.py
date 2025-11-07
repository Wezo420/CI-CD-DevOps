import pytest
from httpx import AsyncClient
from database.models import User, MedicalRecord

@pytest.mark.asyncio
async def test_get_medical_records(async_client: AsyncClient, auth_headers: dict):
    """Test retrieving medical records"""
    response = await async_client.get(
        "/api/patients/me",
        headers=auth_headers
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_medical_record(async_client: AsyncClient, auth_headers: dict):
    """Test creating medical record"""
    response = await async_client.post(
        "/api/patients/create",
        json={
            "diagnosis": "Test diagnosis",
            "treatment": "Test treatment",
            "allergies": ["Penicillin"]
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data

@pytest.mark.asyncio
async def test_unauthorized_access(async_client: AsyncClient):
    """Test unauthorized access"""
    response = await async_client.get("/api/patients/me")
    assert response.status_code == 403
