from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseDBModel


class Users(BaseDBModel):
    __tablename__ = "user_info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    birthday: Mapped[str] = mapped_column(String, default=None)
    about: Mapped[str] = mapped_column(String, nullable=False)


class Holidays(BaseDBModel):
    __tablename__ = "holidays_status"
    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_info.id"), primary_key=True
    )
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    till_date: Mapped[str] = mapped_column(String, nullable=False, default="null")


class MeetInfo(BaseDBModel):
    __tablename__ = "meet_info"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_user_id: Mapped[int] = mapped_column(ForeignKey("user_info.id"))
    second_user_id: Mapped[int] = mapped_column(ForeignKey("user_info.id"))


class Username(BaseDBModel):
    __tablename__ = "tg_usernames"
    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_info.id"), primary_key=True
    )
    username: Mapped[str] = mapped_column(String, nullable=False)


class BanList(BaseDBModel):
    __tablename__ = "ban_list"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    banned_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_info.id"))
    ban_status: Mapped[int] = mapped_column(Integer, default=1)
    date_of_ban: Mapped[str] = mapped_column(default="null")
    comment_to_ban: Mapped[str] = mapped_column(String(500))
    date_of_unban: Mapped[str] = mapped_column(default="null")
    comment_to_unban: Mapped[str] = mapped_column(String(500), default="null")
