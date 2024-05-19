from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, Interval
from app.database import Base


class Project(Base):
    __tablename__ = 'Projects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'), nullable=False)

    creator = relationship('User', back_populates='projects')
    tasks = relationship('Task', back_populates='project')
    members = relationship('User', secondary='ProjectMembers', back_populates='member_projects')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "creator_id": self.creator_id,
        }


class ProjectMember(Base):
    __tablename__ = 'ProjectMembers'

    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('Projects.id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'), primary_key=True)

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "user_id": self.user_id,
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
