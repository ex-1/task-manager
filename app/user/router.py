from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.errors import get_error_user_not_create
from app.session import get_async_session
from app.user.orm import register_user, get_user_from_db
from app.user.schemas import UserIn, UserOut
from app.user.service import hash_password

user = APIRouter(prefix='/user', tags=["User"])


@user.post("/register")
async def register_new_user(
        user_form: UserIn,
        session: Annotated[AsyncSession, Depends(get_async_session)]

):
    user_in_db = await get_user_from_db(user_form.user, session)
    print(user_in_db)
    if user_in_db is not None:
        raise get_error_user_not_create()

    # shifre password
    user_form.password = hash_password(user_form.password)

    return await register_user(user_form, session)
