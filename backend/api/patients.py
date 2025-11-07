# backend/api/patients.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from backend.database.config import get_db
from backend.database.models import MedicalRecord, User, AuditLog
from backend.auth.security import verify_jwt_token

router = APIRouter()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload

@router.get("/me", response_model=list)
async def get_my_records(current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    stmt = select(MedicalRecord).where(MedicalRecord.patient_id == current_user["user_id"])
    res = await db.execute(stmt)
    records = res.scalars().all()
    # FIX: Convert SQLAlchemy objects to dictionaries
    return [
        {
            "id": record.id,
            "patient_id": record.patient_id,
            "diagnosis": record.diagnosis,
            "treatment": record.treatment,
            "allergies": record.allergies,
            "medications": record.medications,
            "lab_results": record.lab_results,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None
        }
        for record in records
    ]

@router.post("/create", response_model=dict)
async def create_medical_record(record: dict, current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new = MedicalRecord(patient_id=current_user["user_id"], **record)
    db.add(new)
    await db.commit()
    await db.refresh(new)
    return {"id": new.id}
