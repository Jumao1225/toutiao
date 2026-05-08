from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, ForeignKey, Text, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )


class Category(Base):
    __tablename__ = "news_category"

    # nullable=False 表示该字段不能为空，unique=True 表示该字段的值必须唯一，autoincrement=True 表示该字段的值会自动递增
    # nullable=Ture 表示该字段可以为空，unique=False 表示该字段的值不需要唯一，autoincrement=False 表示该字段的值不会自动递增
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类id")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序字段，数值越小越靠前")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', sort_order={self.sort_order})>"


class News(Base):
    __tablename__ = "news"

    # 创建索引：提升查询速度 -> 添加目录
    __table_args__ = (
        Index("fk_news_category_idx", "category_id"),   # 高频查询场景
        Index("idx_publish_time", "publish_time")   # 按发布时间排序
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻id")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="新闻图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="新闻作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), nullable=False, comment="分类ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="发布时间")

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', category_id={self.category_id}, views={self.views})>"