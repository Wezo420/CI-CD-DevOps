from backend.database.config import Base
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  # ADD THIS LINE

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    medical_records = relationship(
        "MedicalRecord",
        back_populates="patient",
        foreign_keys="MedicalRecord.patient_id",
        cascade="all, delete-orphan",
    )

    audit_logs = relationship(
        "AuditLog", 
        back_populates="user",
        cascade="all, delete-orphan",
    )


class MedicalRecord(Base):
    __tablename__ = "medical_records"
    __table_args__ = {'extend_existing': True}  # ADD THIS LINE

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("users.id"), nullable=False)
    provider_id = Column(String, ForeignKey("users.id"), nullable=True)
    diagnosis = Column(Text)
    treatment = Column(Text)
    medications = Column(JSON)
    allergies = Column(JSON)
    lab_results = Column(JSON)
    is_encrypted = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = relationship(
        "User",
        foreign_keys=[patient_id],
        back_populates="medical_records",
    )

    provider = relationship(
        "User",
        foreign_keys=[provider_id],
    )


class SecurityScan(Base):
    __tablename__ = "security_scans"
    __table_args__ = {'extend_existing': True}  # ADD THIS LINE
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_type = Column(String)
    repository = Column(String)
    branch = Column(String)
    commit_hash = Column(String, unique=True)
    scan_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    total_issues = Column(Integer, default=0)
    critical_issues = Column(Integer, default=0)
    high_issues = Column(Integer, default=0)
    medium_issues = Column(Integer, default=0)
    low_issues = Column(Integer, default=0)
    results = Column(JSON)
    

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    __table_args__ = {'extend_existing': True}  # ADD THIS LINE
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String, ForeignKey("security_scans.id"))
    title = Column(String)
    description = Column(Text)
    severity = Column(String)
    cvss_score = Column(String)
    cwe_id = Column(String)
    file_path = Column(String)
    line_number = Column(Integer)
    code_snippet = Column(Text)
    remediation = Column(Text)
    discovered_date = Column(DateTime, default=datetime.utcnow)
    fixed_date = Column(DateTime, nullable=True)
    status = Column(String, default="open")


class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"
    __table_args__ = {'extend_existing': True}  # ADD THIS LINE
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    framework = Column(String)
    check_name = Column(String)
    status = Column(String)
    last_checked = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)
    remediation = Column(Text)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {'extend_existing': True}  # ADD THIS LINE
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    action = Column(String)
    resource = Column(String)
    resource_id = Column(String)
    details = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)
    
    user = relationship("User", back_populates="audit_logs")
