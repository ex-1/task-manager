from typing import Annotated

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.services import get_current_user
from app.session import get_async_session
from app.user.schemas import UserOut

project_router = APIRouter(prefix="/project", tags=["Project"])
task_router = APIRouter(prefix="/task", tags=["Task"])
project_router.include_router(task_router)


@project_router.post('/')
def project_create(
        current_user: Annotated[UserOut, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
):
    pass


@task_router.post('/')
def task_create(
        current_user: Annotated[UserOut, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
):
    pass
