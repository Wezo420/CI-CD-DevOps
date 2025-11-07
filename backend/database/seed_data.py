# backend/database/seed_data.py
import logging
import asyncio
from sqlalchemy import select
from database.config import async_session, init_db  # async init & session factory
from database.models import User, MedicalRecord  # your actual models
from auth.security import hash_password

logger = logging.getLogger(__name__)


async def _async_seed():
    """
    Async seeding logic: creates default users and a sample medical record
    only if the DB is empty.
    """
    try:
        # Ensure tables exist (no-op if already created)
        try:
            await init_db()
        except Exception:
            # init_db may not be present / may fail in some CI setups; ignore
            logger.debug("init_db() failed or not available; continuing", exc_info=True)

        async with async_session() as session:
            # Check if any user exists
            q = await session.execute(select(User).limit(1))
            existing = q.scalars().first()
            if existing:
                logger.info("DB already seeded — skipping.")
                return

            # Create users used by tests / default demo accounts
            admin = User(
                username="dr_smith",
                email="dr.smith@hospital.com",
                hashed_password=hash_password("doctor123"),
                full_name="Dr Smith",
                role="doctor",
                is_admin=True,
            )
            staff = User(
                username="nurse_jane",
                email="jane@hospital.com",
                hashed_password=hash_password("staff123"),
                full_name="Nurse Jane",
                role="staff",
                is_admin=False,
            )

            session.add_all([admin, staff])
            await session.flush()  # ensure ids are populated if needed

            # Optional: add a small MedicalRecord sample linked to admin/staff (if your model supports it)
            try:
                sample_record = MedicalRecord(
                    patient_id=admin.id,
                    provider_id=staff.id,
                    diagnosis="Sample diagnosis (seed)",
                    treatment="Sample treatment (seed)",
                    medications=[],
                    allergies=[],
                    lab_results={},
                    is_encrypted=False,
                )
                session.add(sample_record)
            except Exception:
                # If MedicalRecord schema differs, ignore gracefully
                logger.debug("Skipping sample medical record: schema mismatch", exc_info=True)

            await session.commit()
            logger.info("Seeded DB with default users.")
    except Exception as exc:
        logger.warning("Database seeding skipped/failed: %s", exc, exc_info=True)


def seed_database():
    """
    Sync-friendly wrapper so code that calls seed_database() synchronously
    still works (e.g. during some startup paths). It will run the async seeder.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # We're in an existing event loop (e.g., FastAPI startup). Schedule task.
        # Return immediately; startup code that awaited seed_database should call the coroutine directly instead.
        logger.debug("Event loop already running — scheduling async seed task.")
        asyncio.create_task(_async_seed())
    else:
        # No running loop — run the async seeder to completion
        asyncio.run(_async_seed())


# Allow importing the async function directly if needed
async_seed = _async_seed

if __name__ == "__main__":
    # Run manually: python backend/database/seed_data.py
    seed_database()
