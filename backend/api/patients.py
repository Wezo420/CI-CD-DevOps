from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database.config import get_db
from database.models import User, MedicalRecord, AuditLog
from schemas.medical_record import MedicalRecordCreate, MedicalRecordResponse, MedicalRecordUpdate
from auth.security import verify_jwt_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uuid
from datetime import datetime

router = APIRouter()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return payload

@router.get("/me", response_model=List[MedicalRecordResponse])
async def get_my_records(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's medical records"""
    stmt = select(MedicalRecord).where(MedicalRecord.patient_id == current_user["user_id"])
    result = await db.execute(stmt)
    records = result.scalars().all()
    return records

@router.post("/create", response_model=MedicalRecordResponse)
async def create_medical_record(
    record: MedicalRecordCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new medical record"""
    db_record = MedicalRecord(
        id=str(uuid.uuid4()),
        patient_id=current_user["user_id"],
        **record.dict()
    )
    db.add(db_record)
    
    # Audit log
    audit = AuditLog(
        id=str(uuid.uuid4()),
        user_id=current_user["user_id"],
        action="CREATE_RECORD",
        resource="MedicalRecord",
        resource_id=db_record.id,
        details={"timestamp": datetime.utcnow().isoformat()}
    )
    db.add(audit)
    await db.commit()
    await db.refresh(db_record)
    return db_record

@router.get("/{record_id}", response_model=MedicalRecordResponse)
async def get_record(
    record_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get specific medical record"""
    stmt = select(MedicalRecord).where(
        (MedicalRecord.id == record_id) & 
        (MedicalRecord.patient_id == current_user["user_id"])
    )
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()
    
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return record
