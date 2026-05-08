from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite", description="是否收藏当前新闻")


class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId", description="新闻ID")


# 规划两个类：新闻模型类 + 收藏的模型类
class FavoriteNewsItem(NewsItemBase):
    favorite_id: int = Field(alias="favoriteId", description="收藏记录ID")
    favorite_time: datetime = Field(alias="favoriteTime", description="收藏时间")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


# 收藏列表响应模型类
class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItem]
    total: int
    has_more: bool = Field(alias="hasMore", description="是否有更多数据")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
