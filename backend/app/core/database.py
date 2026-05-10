from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings
from typing import AsyncGenerator, Optional

settings = get_settings()

_engine = None
_session_factory = None


def get_engine():
    global _engine
    if _engine is None:
        connect_args = {}
        db_url = settings.database_url
        if db_url.startswith("sqlite"):
            connect_args["check_same_thread"] = False
            connect_args["timeout"] = 30
        elif db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        _engine = create_async_engine(
            db_url,
            echo=settings.debug,
            connect_args=connect_args if connect_args else {},
            pool_pre_ping=True,
        )
    return _engine


def get_session_factory():
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _session_factory


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    engine = get_engine()
    await engine.dispose()
