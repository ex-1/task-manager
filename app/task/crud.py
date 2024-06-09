from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import *
from app.task.schemas import *


async def get_projects(db: AsyncSession):
    result = await db.execute(select(Project))
    return result.scalars().all()


async def get_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    db_project = result.scalars().first()
    return db_project


async def get_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()


async def create_project(db: AsyncSession, project: ProjectCreate, user_id: int):
    db_project = Project(**project.dict(), creator_id=user_id)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


async def update_project(db: AsyncSession, project_id: int, project: ProjectUpdate):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    db_project = result.scalars().first()
    if db_project:
        for key, value in project.dict().items():
            setattr(db_project, key, value)
        await db.commit()
        await db.refresh(db_project)
    return db_project


async def delete_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    db_project = result.scalars().first()
    if db_project:
        await db.delete(db_project)
        await db.commit()
    return db_project


async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    return result.scalars().first()


async def create_task(db: AsyncSession, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(db: AsyncSession, task_id: int, task: TaskUpdate):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    db_task = result.scalars().first()
    if db_task:
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        await db.commit()
        await db.refresh(db_task)
    return db_task


async def delete_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    db_task = result.scalars().first()
    if db_task:
        await db.delete(db_task)
        await db.commit()
    return db_task
