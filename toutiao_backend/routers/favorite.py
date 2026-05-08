from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud.favorite import is_news_favorite, add_news_favorite, remove_news_favorite, get_favorite_list, clear_favorite_list
from models.users import User
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteListResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


@router.get("/check")
async def check_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    # 验证登录状态 -> 检查用户是否收藏当前新闻
    is_favorite = await is_news_favorite(db, user.id, news_id)
    return success_response(message="检查收藏状态成功", data=FavoriteCheckResponse(isFavorite=is_favorite))


# 请求体用 Pydantic 模型来验证 -> 添加收藏记录
@router.post("/add")
async def add_favorite(
        data: FavoriteAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    # 验证登录状态 -> 添加收藏记录
    result = await add_news_favorite(db, user.id, data.news_id)
    return success_response(message="添加收藏成功", data=result)


@router.delete("/remove")
async def remove_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    result = await remove_news_favorite(db, user.id, news_id)
    if not result:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="未找到收藏记录，无法取消收藏")
    return success_response(message="取消收藏成功")


# 获取收藏列表
@router.get("/list")
async def list_favorites(
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize", description="每页数量"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    rows, total = await get_favorite_list(db, user.id, page, page_size)
    favorite_list = [{
        **news.__dict__,
        "favorite_time": favorite_time,
        "favorite_id": favorite_id
    } for news, favorite_time, favorite_id in rows]
    has_more = (page * page_size) < total

    data = FavoriteListResponse(list=favorite_list, total=total, has_more=has_more)
    return success_response(message="获取收藏列表成功", data=data)


# 清空收藏列表
@router.delete("/clear")
async def clear_favorites(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    count = await clear_favorite_list(db, user.id)
    return success_response(message=f"成功删除{count}条收藏记录")
