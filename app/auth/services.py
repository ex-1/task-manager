from datetime import timezone, datetime, timedelta
from typing import Annotated
from fastapi import Depends
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import TokenIn, TokenOut
from app.config import settings
from app.session import get_async_session
from app.auth.constants import oauth2_scheme
from app.user.orm import get_user_by_username
from app.user.schemas import UserSchema, UserOut
from app.user.services import compare_password


def jwt_code(username: str) -> TokenOut:
    dict_present = TokenIn(
        sub=username,
        exp=datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    jwt_token = jwt.encode(
        dict_present.model_dump(), settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return TokenOut(access_token=jwt_token)


def jwt_decode(token: str) -> TokenIn:
    dict_presents = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    return TokenIn.model_validate(dict_presents)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> UserOut:
    decode_token = jwt_decode(token)
    user = await get_user_by_username(decode_token.sub, session)
    return UserOut(**user.model_dump())


async def authenticate_user(user: UserSchema, session: AsyncSession) -> UserOut | bool:
    get_user = await get_user_by_username(user.username, session)
    if get_user is None:
        return False
    if not compare_password(user.password, get_user.hashed_password):
        return False
    return get_user
