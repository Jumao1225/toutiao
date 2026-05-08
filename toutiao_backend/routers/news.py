from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import news, news_cache

# 创建 APIRouter 实例
# prefix 参数指定了路由的前缀，tags 参数用于给路由分组，方便在文档中查看
# tags 参数是一个列表，可以包含多个标签，标签可以用来对路由进行分类，在自动生成的 API 文档中会显示这些标签
router = APIRouter(prefix="/api/news", tags=["news"])


# 接口实现流程
# 1.模块化路由 + API接口规范文档
# 2.定义模型类 -> 数据库表 （数据库设计文档）
# 3.在 crud 文件夹里面创建文件，封装操作数据库的方法
# 4.在路由处理函数中调用 crud 封装好的方法，响应结果


@router.get("/categories")
async def get_news_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # 先获取数据库里面新闻分类数据 -> 先定义模型类 -> 封装查询数据的方法
    categories = await news_cache.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "成功获取新闻分类",
        "data": categories
    }


@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(default=10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db)
):
    # 处理分页规则 -> 查询新闻列表 -> 计算总量 -> 计算是否有更多
    offset = (page - 1) * page_size
    news_list = await news_cache.get_news_list(db, category_id, offset, limit=page_size)
    total = await news.get_news_count(db, category_id)
    # (跳过的 + 当前列表里面的数量) < 总量 -> 还有更多
    has_more = (offset + len(news_list)) < total
    return {
        "code": 200,
        "message": "成功获取新闻列表",
        "data": {
            "list": news_list,
            "total": total,
            "hasMore": has_more
        }
    }


@router.get("/detail")
async def get_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    # 获取当前新闻详情 + 增加 1 次浏览量 + 相关新闻 （同分类 id 的新闻）
    news_detail = await news.get_news_detail(db, news_id)

    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    views_res = await news.increase_news_views(db, news_detail.id)
    if not views_res:
        raise HTTPException(status_code=404, detail="新闻不存在")

    relate_news = await news.get_related_news(db, news_detail.category_id, news_detail.id)

    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": relate_news
        }
    }


