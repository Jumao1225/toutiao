from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category, News
from cache.news_cache import get_cached_categories, set_cache_categories, get_cache_news_list, set_cache_news_list


# offset(跳过数量)
from schemas.base import NewsItemBase


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        print(">>> [DEBUG] 命中缓存，直接返回数据")  # 添加此行
        return cached_categories

    print(">>> [DEBUG] 缓存未命中，开始查询数据库")  # 添加此行
    stmt = select(Category).offset(skip).limit(limit)  # offset 用于指定查询结果的起始位置，limit 用于指定查询结果的最大数量
    result = await db.execute(stmt)  # 执行查询语句
    categories = result.scalars().all()  # ORM scalars() 方法用于提取查询结果中的标量值（即单个列的值），all() 方法用于获取所有结果并返回一个列表

    # 写入缓存
    if categories:  # 如果查询结果不为空，则将数据写入缓存
        categories = jsonable_encoder(categories)
        await set_cache_categories(categories)

    # 返回数据
    return categories


async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 先查缓存
    # 跳过的数量skip = (页码 - 1) * 每页数量 -> 页码 = 跳过的数量 // 每页数量 + 1
    # await get_cache_news_list(分类id, 页码, 每页数量)
    page = skip // limit + 1
    cached_list = await get_cache_news_list(category_id, page, limit)   # 缓存数据 json
    if cached_list:
        print(">>> [DEBUG] 列表命中缓存，直接返回数据")  # 添加此行
        # return cached_list # 要的是 ORM 格式
        return [News(**item) for item in cached_list]

    # 查询的是指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    # 写入缓存
    if news_list:
        # 先把 ORM 数据 转换 字典才能写入缓存
        # ORM 转成 Pydantic 模型，再转成字典，最后写入缓存
        # by_alias=False 不使用别名，保存 python风格，因为 Redis 数据是给后端用的
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, page, limit, news_data)  # 分类id、页码、每页数量、数据列表

    return news_list


async def get_news_count(db: AsyncSession, category_id: int):
    # 查询指定分类下的新闻数量
    stmt = select(func.count()).where(News.category_id == category_id)
    result = await db.execute(stmt)
    # news_count = result.scalar()  # scalar() 方法用于获取查询结果中的单个标量值，如果查询结果中没有值，则返回 None；如果查询结果中有多个值，则会抛出异常
    news_count = result.scalar_one()  # scalar_one() 只能有一个结果，否则报错
    return news_count


async def get_news_detail(db: AsyncSession, news_id: int):
    # 查询指定 id 的新闻详情
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def increase_news_views(db: AsyncSession, news_id: int):
    # 增加指定 id 新闻的浏览量
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()

    # 更新 -> 检查数据库是否真的命中了数据 -> 命中了返回Ture，否则返回 False
    return result.rowcount > 0


async def get_related_news(db: AsyncSession, category_id: int, news_id: int, limit: int = 5):
    # 查询同分类下的相关新闻，排除当前新闻
    # order_by 排序 -> 浏览量和发布时间
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc(),  # 默认是升序，desc 是降序
        News.publish_time.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()

    # 列表推导式 推导出新闻的核心数据，然后再 return
    return [{
        "id": news_detail.id,
        "title": news_detail.title,
        "content": news_detail.content,
        "image": news_detail.image,
        "author": news_detail.author,
        "publishTime": news_detail.publish_time,
        "categoryId": news_detail.category_id,
        "views": news_detail.views,
    } for news_detail in related_news]

    # return related_news
