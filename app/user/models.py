from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy import Integer, String

from app.user.schemas import UserOut


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)

    def to_dict(self) -> UserOut:
        return UserOut.from_orm(self)

    def get_hashed_password(self) -> Mapped[str]:
        return self.hashed_password

