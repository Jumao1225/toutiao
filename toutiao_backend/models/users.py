from datetime import datetime
from typing import Optional

from sqlalchemy import Index, DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    __table_args__ = (
        Index('username_UNIQUE', 'username'),
        Index('phone_UNIQUE', 'phone')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="用户id")
    username: Mapped[str] = mapped_column(unique=True, nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(nullable=False, comment="密码")
    nickname: Mapped[Optional[str]] = mapped_column(nullable=True, comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(nullable=True, comment="头像URL")
    gender: Mapped[Optional[int]] = mapped_column(nullable=True, comment="性别，0-未知，1-男，2-女")
    bio: Mapped[str] = mapped_column(nullable=True, comment="个人简介")
    phone: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True, comment="手机号")

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now,
                                                 comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now,
                                                 onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class UserToken(Base):
    __tablename__ = "user_token"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="用户token id")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户id")
    token: Mapped[str] = mapped_column(String(255), nullable=False, comment="用户token")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now,
                                                 comment="创建时间")

    def __repr__(self):
        return f"<UserToken(id={self.id}, user_id={self.user_id}, token='{self.token}')>"
