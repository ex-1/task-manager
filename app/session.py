from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.config import settings

DATABASE_URL = (
    f"{settings.P_ASYNC_DRIVER}://{settings.P_USER}:{settings.P_PASS}"
    f"@{settings.P_HOST}:{settings.P_PORT}/{settings.P_DB}"
)
engine = create_async_engine(DATABASE_URL)

session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
