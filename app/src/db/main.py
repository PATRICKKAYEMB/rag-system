from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker




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
async def get_session()->AsyncSession:
    Session = sessionmaker(
        bind=asyn_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session


       