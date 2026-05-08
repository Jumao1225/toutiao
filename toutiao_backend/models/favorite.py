from datetime import datetime

from sqlalchemy import Index, UniqueConstraint, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.news import News
from models.users import User


class Base(DeclarativeBase):
    pass


class Favorite(Base):
    __tablename__ = "favorite"

    # 创建联合唯一索引，确保同一用户对同一新闻只能收藏一次，同时为 user_id 和 news_id 创建单列索引，提升查询性能
    # UniqueConstraint：唯一约束，当前新闻只能收藏一次
    __table_args__ = (
        UniqueConstraint('user_id', 'news_id', name='user_news_unique'),
        Index('fk_favorite_user_idx', 'user_id'),
        Index('fk_favorite_news_idx', 'news_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="收藏ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="收藏时间")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, create_at={self.created_at})>"
