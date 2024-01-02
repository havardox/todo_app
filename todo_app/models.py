import datetime

from sqlalchemy import ForeignKey, SmallInteger, String, Boolean, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todo_app.db import Base


# Logic: For optional string fields, provide a default value of "".
# For required string fields, refrain from setting a default value to ensure INSERT operations fail when not all columns
# are explicitly specified. This prevents inadvertent empty string assignments.


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    last_name: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    hashed_password: Mapped[str] = mapped_column(String(60))
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    todos: Mapped[list["Todo"]] = relationship(back_populates="user")


class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(2048), nullable=False, default="")
    priority: Mapped[int] = mapped_column(SmallInteger)
    date_due: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    time_due: Mapped[datetime.time] = mapped_column(Time(timezone=True), nullable=True)
    done: Mapped[bool] = mapped_column(Boolean)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="todos", foreign_keys=[user_id])
