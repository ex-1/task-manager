from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services import get_current_user
from app.errors import (
    get_error_user_in_db,
    get_404_user_not_found,
    get_error_user_not_create,
)
from app.session import get_async_session
from app.user.schemas import UserIn, UserOut, CreatedUserMessage
from app.user.orm import create_user, get_user_by_username, get_user_by_id

user_router = APIRouter(prefix="/user", tags=["User"])
user_templates_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/profile/me", response_model=UserOut)
def user_me(current_user: Annotated[UserOut, Depends(get_current_user)]) -> UserOut:
    return current_user


@user_router.post("/register")
async def user_register(
    user: UserIn, session: AsyncSession = Depends(get_async_session)
) -> CreatedUserMessage:
    if await get_user_by_username(user.username, session) is not None:
        raise get_error_user_in_db()
    try:
        new_user = await create_user(user, session)
    except IntegrityError:
        raise get_error_user_not_create()
    return new_user


@user_router.get("/profile/{user_id}", response_model=UserOut)
async def user_profile(
    # current_user: Annotated[UserOut, Depends(get_current_user)],
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> UserOut:
    get_user = await get_user_by_id(user_id, session)
    if get_user is None:
        raise get_404_user_not_found()
    return get_user

