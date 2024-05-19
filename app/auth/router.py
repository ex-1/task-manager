from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import TokenOut
from app.auth.services import authenticate_user, jwt_code
from app.errors import get_error_user_not_authenticate
from app.session import get_async_session
from app.user.schemas import UserSchema


auth_router = APIRouter(prefix="/security", tags=["Auth"])
auth_templates_router = APIRouter(prefix="/login", tags=["User"])


@auth_router.post("/token")
async def new_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> TokenOut:
    user = UserSchema(username=form_data.username, password=form_data.password)
    get_user = await authenticate_user(user=user, session=session)
    if not get_user:
        raise get_error_user_not_authenticate()
    return jwt_code(user.username)
