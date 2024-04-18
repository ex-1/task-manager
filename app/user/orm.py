from sqlalchemy import select
from app.user.models import User
from app.user.schemas import UserIn, UserOut
from sqlalchemy.ext.asyncio import AsyncSession


async def register_user(user: UserIn, session: AsyncSession) -> int:
    new_user = User(**user.dict())
    session.add(new_user)
    await session.commit()
    return new_user.id


async def get_user_from_db(user_query: str | int, session: AsyncSession) -> UserOut | None:
    if isinstance(user_query, str):
        query_column = User.name
    elif isinstance(user_query, int):
        query_column = User.id
    else:
        # Handle unsupported types or invalid queries
        raise ValueError("Unsupported user query type")

    user = (await session.execute(select(User).where(query_column == user_query))).scalar_one_or_none()
    return user.to_dict() if user else None
