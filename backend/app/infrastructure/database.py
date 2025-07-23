from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession 
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
