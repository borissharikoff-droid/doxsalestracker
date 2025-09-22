from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.database_url, future=True, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def init_db() -> None:
    from app import models  # noqa: F401
    async with engine.begin() as conn:
<<<<<<< HEAD
        await conn.run_sync(Base.metadata.create_all)
=======
        await conn.run_sync(Base.metadata.create_all)
>>>>>>> d26e15bb748e2dacfacaec01384eaf20197cfb35
