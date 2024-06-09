from typing import Annotated, List

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.services import get_current_user
from app.errors import get_error_project_not_found, get_error_auth_for_update, get_error_task_not_found, \
    get_error_task_auth_for_update
from app.session import get_async_session
from app.task.crud import create_project, create_task, get_projects, update_project, get_project, delete_project, \
    get_tasks, get_task, update_task, delete_task
from app.task.schemas import ProjectCreate, ProjectOut, TaskOut, TaskCreate, ProjectUpdate, TaskUpdate
from app.user.schemas import UserOut

project_router = APIRouter(prefix="/project", tags=["Project"])
task_router = APIRouter(prefix="/task", tags=["Task"])


@project_router.post('/', response_model=ProjectOut)
async def project_create(
    project: ProjectCreate,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    return await create_project(session, project, current_user.id)


@task_router.post('/', response_model=TaskOut)
async def task_create(
    task: TaskCreate,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    task.performer_id = current_user.id
    return await create_task(session, task)


@project_router.post('/', response_model=ProjectOut)
async def project_create(
    project: ProjectCreate,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    return await create_project(session, project, current_user.id)


@project_router.get('/', response_model=List[ProjectOut])
async def project_read_all(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_projects(session)


@project_router.get('/{project_id}', response_model=ProjectOut)
async def project_read(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await get_project(session, project_id)
    if not project:
        get_error_project_not_found()
    return project


@project_router.put('/{project_id}', response_model=ProjectOut)
async def project_update(
    project_id: int,
    project: ProjectUpdate,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    db_project = await get_project(session, project_id)
    if not db_project:
        raise get_error_project_not_found()
    if db_project.creator_id != current_user.id:
        raise get_error_auth_for_update()
    return await update_project(session, project_id, project)


@project_router.delete('/{project_id}', response_model=ProjectOut)
async def project_delete(
    project_id: int,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    db_project = await get_project(session, project_id)
    if not db_project:
        raise get_error_project_not_found()
    if db_project.creator_id != current_user.id:
        raise get_error_auth_for_update()
    return await delete_project(session, project_id)


@task_router.post('/', response_model=TaskOut)
async def task_create(
    task: TaskCreate,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    task.performer_id = current_user.id
    return await create_task(session, task)


@task_router.get('/', response_model=List[TaskOut])
async def task_read_all(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_tasks(session)


@task_router.get('/{task_id}', response_model=TaskOut)
async def task_read(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    task = await get_task(session, task_id)
    if not task:
        raise get_error_task_not_found()
    return task


@task_router.put('/{task_id}', response_model=TaskOut)
async def task_update(
    task_id: int,
    task: TaskUpdate,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    db_task = await get_task(session, task_id)
    if not db_task:
        raise get_error_task_not_found()
    if db_task.performer_id != current_user.id:
        raise get_error_task_auth_for_update()
    return await update_task(session, task_id, task)


@task_router.delete('/{task_id}', response_model=TaskOut)
async def task_delete(
    task_id: int,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    db_task = await get_task(session, task_id)
    if not db_task:
        raise get_error_task_not_found()
    if db_task.performer_id != current_user.id:
        raise get_error_task_auth_for_update()
    return await delete_task(session, task_id)

