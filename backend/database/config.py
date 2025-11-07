import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger(__name__)

# Use DATABASE_URL env var if set; otherwise fall back to a local SQLite for CI/tests.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./test.db"
)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_ECHO", "False").lower() == "true",
    future=True,
)

# Session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models - SINGLE SOURCE OF TRUTH
Base = declarative_base()

async def init_db():
    """Initialize database tables (create_all)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")

async def get_db():
    """Async dependency to yield a DB session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
