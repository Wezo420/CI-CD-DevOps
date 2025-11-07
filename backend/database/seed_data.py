# backend/database/seed_data.py
import os
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

# Use absolute import path
from backend.database.models import User, MedicalRecord
from backend.database.config import async_session
from backend.auth.security import hash_password

async def seed_database():
    """Seed the database with initial data"""
    async with async_session() as session:
        # Check if we already have users
        result = await session.execute("SELECT COUNT(*) FROM users")
        count = result.scalar()
        
        if count == 0:
            # Create admin user
            admin_user = User(
                username="admin",
                email="admin@medical.com",
                hashed_password=hash_password("admin123"),
                full_name="System Administrator",
                is_admin=True,
                role="admin"
            )
            
            # Create doctor user
            doctor_user = User(
                username="dr_smith",
                email="dr.smith@medical.com", 
                hashed_password=hash_password("doctor123"),
                full_name="Dr. John Smith",
                role="doctor"
            )
            
            # Create patient user
            patient_user = User(
                username="patient1",
                email="patient1@example.com",
                hashed_password=hash_password("patient123"),
                full_name="Jane Doe",
                role="user"
            )
            
            session.add_all([admin_user, doctor_user, patient_user])
            await session.commit()
            
            # Create sample medical record
            medical_record = MedicalRecord(
                patient_id=patient_user.id,
                provider_id=doctor_user.id,
                diagnosis="Annual checkup",
                treatment="Routine physical examination",
                allergies=["None"],
                is_encrypted=False
            )
            
            session.add(medical_record)
            await session.commit()
            
            print("Database seeded successfully!")
        else:
            print("Database already seeded, skipping...")

# For sync compatibility
def seed_database_sync():
    """Sync wrapper for seed_database"""
    asyncio.run(seed_database())
