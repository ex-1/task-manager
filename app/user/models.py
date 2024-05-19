from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    projects = relationship('Project', back_populates='creator')
    tasks = relationship('Task', back_populates='performer')
    comments = relationship('Comment', back_populates='author')
    passport_data = relationship('PassportData', uselist=False, back_populates='user')
    member_projects = relationship('Project', secondary='ProjectMembers', back_populates='members')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "avatar": self.avatar,
            "hashed_password": self.hashed_password,
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
    passport_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    issue_date: Mapped[str] = mapped_column(Date, nullable=False)
    expiration_date: Mapped[str] = mapped_column(Date, nullable=False)
    place_of_issue: Mapped[str] = mapped_column(String(255), nullable=False)

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
