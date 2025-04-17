from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

from app.core.config import settings

if settings.DATABASE_URL is None:
    raise ValueError("DATABASE_URL must be set in the environment variables or .env file.")

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG_MODE, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides an AsyncSession for a request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            pass
