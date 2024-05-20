from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.services import hash_password
from app.models import User, PassportData
from app.user.schemas import UserIn, UserOut, CreatedUserMessage, UserOutWithPassword


async def create_user(user: UserIn, session: AsyncSession) -> CreatedUserMessage:
    new_user = User(
        username=user.username,
        name=user.name,
        hashed_password=hash_password(user.password),
    )
    session.add(new_user)
    await session.commit()
    new_passport_data = PassportData(user_id=new_user.id)
    session.add(new_passport_data)
    await session.commit()
    return CreatedUserMessage()


async def put_user(user: UserOut, session: AsyncSession):
    pass


async def get_user_by_username(
    username: str, session: AsyncSession
) -> UserOutWithPassword | None:
    user = (
        await session.execute(select(User).where(User.username == username))
    ).scalar_one_or_none()
    if user:
        return UserOutWithPassword(**user.to_dict())
    return None


async def get_user_by_id(user_id: int,
                         session: AsyncSession) -> UserOut | None:
    user = (
        await session.execute(select(User).where(User.id == user_id))
    ).scalar_one_or_none()
    if user:
        return UserOut(**user.to_dict())
    return None
