from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.user.services import hash_password
from app.models import User, PassportData
from app.user.schemas import UserIn, UserOut, CreatedUserMessage, UserOutWithPassword, UserPut


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


async def put_user(user_id: int, user_input: UserPut, session: AsyncSession):
    user = (
        await session.execute(select(User).where(User.id == user_id)
                              .options(joinedload(User.passport_data)))
    ).scalar_one()
    # change user
    if user_input.username:
        user.username = user_input.username
    if user_input.name:
        user.name = user_input.name
    # change passport
    if not user_input.passport_data:
        return user_id

    if user.passport_data is None:
        user.passport_data = PassportData()

    if user_input.passport_data.passport_number:
        user.passport_data.passport_number = user_input.passport_data.passport_number
    if user_input.passport_data.issue_date:
        user.passport_data.issue_date = user_input.passport_data.issue_date
    if user_input.passport_data.expiration_date:
        user.passport_data.expiration_date = user_input.passport_data.expiration_date
    if user_input.passport_data.place_of_issue:
        user.passport_data.place_of_issue = user_input.passport_data.place_of_issue

    await session.commit()
    return user_id


async def get_user_by_username(
    username: str, session: AsyncSession
) -> UserOutWithPassword | None:
    user = (
        await session.execute(select(User).where(User.username == username))
    ).scalar_one_or_none()
    if user:
        return UserOutWithPassword(
            username=user.username,
            id=user.id,
            name=user.name,
            hashed_password=user.hashed_password
        )
    return None


async def get_user_by_id(user_id: int,
                         session: AsyncSession) -> UserPut | None:
    user = (
        await session.execute(select(User).where(User.id == user_id)
                              .options(joinedload(User.passport_data)))
    ).scalar_one_or_none()
    if user:
        return UserPut(**(await user.to_dict()), passport_data=user.passport_data.to_dict())
    return None

