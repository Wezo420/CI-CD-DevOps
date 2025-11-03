from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class SecurityScanCreate(BaseModel):
    scan_type: str  # sast, dast, dependency, secrets, container
    repository: str
    branch: str
    commit_hash: str
    total_issues: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    results: Optional[Dict[str, Any]] = None

class SecurityScanResponse(BaseModel):
    id: str
    scan_type: str
    repository: str
    scan_date: datetime
    status: str
    total_issues: int
    critical_issues: int
    results: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True

class VulnerabilityResponse(BaseModel):
    id: str
    title: str
    severity: str
    cvss_score: Optional[str]
    file_path: str
    remediation: Optional[str]
    status: str
    
    class Config:
        from_attributes = True
