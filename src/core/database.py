from collections.abc import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.core.config import settings  # Your global Pydantic Settings instance

# 1. Create the asynchronous database engine
# settings.DATABASE_URL might be: postgresql+asyncpg://user:pass@localhost:5432/dbname
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,          # True in local development for logging SQL queries
    pool_size=20,                    # Production connection pool size
    max_overflow=10,                # Allow temporary bursts of extra connections
    pool_pre_ping=True,             # Checks connection health before using it
)

# 2. Create the session maker factory
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,         # Prevents errors when accessing attributes after commit
    autoflush=False,
)

# 3. Create the Declarative Base class that models inherit from
class Base(DeclarativeBase):
    metadata = MetaData(schema="cert_db")
