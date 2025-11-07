from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from datetime import datetime, timedelta

from backend.database.config import get_db
from backend.database.models import SecurityScan, Vulnerability, ComplianceCheck
from backend.schemas.security_scan import SecurityScanCreate, SecurityScanResponse, VulnerabilityResponse
from backend.auth.security import verify_jwt_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uuid

router = APIRouter()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return payload

@router.get("/scans", response_model=List[SecurityScanResponse])
async def get_scans(
    skip: int = 0,
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get recent security scans"""
    stmt = select(SecurityScan).order_by(desc(SecurityScan.scan_date)).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/scans", response_model=SecurityScanResponse)
async def create_scan(
    scan: SecurityScanCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Store security scan results"""
    db_scan = SecurityScan(
        id=str(uuid.uuid4()),
        status="completed",
        **scan.dict()
    )
    db.add(db_scan)
    await db.commit()
    await db.refresh(db_scan)
    return db_scan

@router.get("/vulnerabilities", response_model=List[VulnerabilityResponse])
async def get_vulnerabilities(
    severity: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get vulnerabilities"""
    if severity:
        stmt = select(Vulnerability).where(Vulnerability.severity == severity)
    else:
        stmt = select(Vulnerability)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/compliance", response_model=dict)
async def get_compliance_status(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get compliance framework status"""
    stmt = select(ComplianceCheck)
    result = await db.execute(stmt)
    checks = result.scalars().all()
    
    frameworks = {}
    for check in checks:
        if check.framework not in frameworks:
            frameworks[check.framework] = {"passed": 0, "failed": 0, "total": 0}
        frameworks[check.framework]["total"] += 1
        if check.status == "pass":
            frameworks[check.framework]["passed"] += 1
        else:
            frameworks[check.framework]["failed"] += 1
    
    return frameworks
