# 新闻相关的缓存方法：新闻分类的读取和写入
# key - value
from typing import List, Dict, Any, Optional

from config.redis_conf import get_cache_json, set_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news:list"  # news:list:分类id:页码:每页数量


# 获取新闻分类缓存
async def get_cached_categories():
    return await get_cache_json(CATEGORIES_KEY)


# 写入新闻分类缓存：缓存的数据 + 过期时间
# 分类、配置：7200；列表：600；详情：1800；验证码：120 -- 数据越稳定，缓存越持久
# 过期时间分配的不一样，可以避免所有的key同时过期，造成缓存雪崩
async def set_cache_categories(
        data: List[Dict[str, Any]],
        expire: int = 7200  # 2小时
):
    return await set_cache(CATEGORIES_KEY, data, expire)


# 写入缓存-新闻列表 key = news_list:分类id:页码:每页数量 + 列表数据 + 过期时间
async def set_cache_news_list(
        category_id: Optional[int],
        page: int,
        page_size: int,
        news_list: List[Dict[str, Any]],
        expire: int = 600  # 10分钟
):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}:{category_part}:{page}:{page_size}"
    await set_cache(key, news_list, expire)


# 读取缓存-新闻列表
async def get_cache_news_list(
        category_id: Optional[int],
        page: int,
        page_size: int
):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}:{category_part}:{page}:{page_size}"
    return await get_cache_json(key)





