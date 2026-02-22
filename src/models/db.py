from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseDBModel
from sqlalchemy import Integer, String, ForeignKey

class Users(BaseDBModel):
    __tablename__ = "user_info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    birthday: Mapped[str] = mapped_column(String, default=None)
    about: Mapped[str] = mapped_column(String, nullable=False)

class Holidays(BaseDBModel):
    __tablename__ = "holidays_status"
    id: Mapped[int] = mapped_column(Integer, ForeignKey("user_info.id"), primary_key=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    till_date: Mapped[str] = mapped_column(String, nullable=False, default="null")