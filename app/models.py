from datetime import date

from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, Date, Table, Column, Interval
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base

project_members_table = Table(
    'ProjectMembers', Base.metadata,
    Column('project_id', Integer, ForeignKey('Projects.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('Users.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    projects = relationship('Project', back_populates='creator')
    tasks = relationship('Task', back_populates='performer')
    comments = relationship('Comment', back_populates='author')
    passport_data = relationship('PassportData', uselist=False, back_populates='user', lazy='selectin')
    member_projects = relationship('Project', secondary=project_members_table, back_populates='members')

    async def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "avatar": self.avatar,
            "hashed_password": self.hashed_password,
        }


class Project(Base):
    __tablename__ = 'Projects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'), nullable=False)

    creator = relationship('User', back_populates='projects')
    tasks = relationship('Task', back_populates='project')
    members = relationship('User', secondary=project_members_table , back_populates='member_projects')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "creator_id": self.creator_id,
        }


class Task(Base):
    __tablename__ = 'Tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    time_in_status: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    timer_task: Mapped[str] = mapped_column(Interval, nullable=False)
    start_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    deadline: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    end_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))
    performer_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('Projects.id'), nullable=False)
    parent_task_id: Mapped[int] = mapped_column(Integer, ForeignKey('Tasks.id'))

    performer = relationship('User', back_populates='tasks')
    project = relationship('Project', back_populates='tasks')
    parent_task = relationship('Task', remote_side=[id])
    comments = relationship('Comment', back_populates='task')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "time_in_status": self.time_in_status,
            "timer_task": self.timer_task,
            "start_at": self.start_at,
            "deadline": self.deadline,
            "end_at": self.end_at,
            "performer_id": self.performer_id,
            "project_id": self.project_id,
            "parent_task_id": self.parent_task_id,
        }


class Comment(Base):
    __tablename__ = 'Comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('Tasks.id'), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'), nullable=False)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default='now()')

    task = relationship('Task', back_populates='comments')
    author = relationship('User', back_populates='comments')

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "author_id": self.author_id,
            "content": self.content,
            "created_at": self.created_at,
        }


class Audit(Base):
    __tablename__ = 'Audit'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    table_name: Mapped[str] = mapped_column(String(255), nullable=False)
    row_id: Mapped[int] = mapped_column(Integer, nullable=False)
    operation: Mapped[str] = mapped_column(String(10), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), default='now()')

    def to_dict(self):
        return {
            "id": self.id,
            "table_name": self.table_name,
            "row_id": self.row_id,
            "operation": self.operation,
            "username": self.username,
            "timestamp": self.timestamp,
        }


class PassportData(Base):
    __tablename__ = 'PassportData'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'), unique=True, nullable=False)
    passport_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    issue_date: Mapped[date] = mapped_column(Date, nullable=True)
    expiration_date: Mapped[date] = mapped_column(Date, nullable=True)
    place_of_issue: Mapped[str] = mapped_column(String(255), nullable=True)

    user = relationship('User', back_populates='passport_data')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "passport_number": self.passport_number,
            "issue_date": self.issue_date,
            "expiration_date": self.expiration_date,
            "place_of_issue": self.place_of_issue,
        }
