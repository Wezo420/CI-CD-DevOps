from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database.config import Base
import uuid
import os
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test_sync.db")

def make_sync_engine(url: str):
    try:
        e = create_engine(url, echo=False, pool_pre_ping=True, future=True)
        return e
    except Exception as exc:
        logger.warning(f"Failed to create engine for {url}: {exc}")
        fallback = "sqlite:///./test_sync.db"
        logger.info(f"Falling back to SQLite for CI/tests: {fallback}")
        return create_engine(fallback, echo=False, future=True)

engine = make_sync_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    role = Column(String, default="user")  # user, doctor, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    medical_records = relationship("MedicalRecord", back_populates="patient")
    audit_logs = relationship("AuditLog", back_populates="user")

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey("users.id"), nullable=False)
    provider_id = Column(String, ForeignKey("users.id"))
    diagnosis = Column(Text)
    treatment = Column(Text)
    medications = Column(JSON)
    allergies = Column(JSON)
    lab_results = Column(JSON)
    is_encrypted = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    patient = relationship("User", foreign_keys=[patient_id], back_populates="medical_records")

class SecurityScan(Base):
    __tablename__ = "security_scans"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_type = Column(String, index=True)  # sast, dast, dependency, secrets, container
    repository = Column(String, index=True)
    branch = Column(String)
    commit_hash = Column(String, unique=True)
    scan_date = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String)  # pending, in_progress, completed, failed
    total_issues = Column(Integer, default=0)
    critical_issues = Column(Integer, default=0)
    high_issues = Column(Integer, default=0)
    medium_issues = Column(Integer, default=0)
    low_issues = Column(Integer, default=0)
    results = Column(JSON)
    
class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scan_id = Column(String, ForeignKey("security_scans.id"))
    title = Column(String, index=True)
    description = Column(Text)
    severity = Column(String)  # critical, high, medium, low
    cvss_score = Column(String)
    cwe_id = Column(String)
    file_path = Column(String)
    line_number = Column(Integer)
    code_snippet = Column(Text)
    remediation = Column(Text)
    discovered_date = Column(DateTime, default=datetime.utcnow)
    fixed_date = Column(DateTime, nullable=True)
    status = Column(String, default="open")  # open, fixed, wontfix

class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    framework = Column(String, index=True)  # hipaa, soc2, gdpr, pci-dss
    check_name = Column(String)
    status = Column(String)  # pass, fail, warning
    last_checked = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)
    remediation = Column(Text)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    action = Column(String, index=True)
    resource = Column(String)
    resource_id = Column(String)
    details = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String)
    
    user = relationship("User", back_populates="audit_logs")
