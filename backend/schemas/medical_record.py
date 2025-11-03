from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MedicalRecordCreate(BaseModel):
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    medications: Optional[List[Dict[str, Any]]] = None
    allergies: Optional[List[str]] = None
    lab_results: Optional[Dict[str, Any]] = None

class MedicalRecordResponse(BaseModel):
    id: str
    patient_id: str
    diagnosis: Optional[str]
    treatment: Optional[str]
    is_encrypted: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MedicalRecordUpdate(BaseModel):
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    medications: Optional[List[Dict[str, Any]]] = None
    allergies: Optional[List[str]] = None
