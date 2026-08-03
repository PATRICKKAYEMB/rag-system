from sqlmodel import create_engine, SQLModel, Session,text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from src.config import config



engine = AsyncEngine(
   create_engine (
        config.DATABASE_URL, echo=True
    ) 
    )

async def init_db():
    async with engine.begin() as conn:
        from src.bookds.model import Book
        await conn.run_sync(
            SQLModel.metadata.create_all
        )

       