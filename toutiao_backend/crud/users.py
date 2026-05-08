import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User, UserToken
from schemas.users import UserRegisterRequest, UserUpdateRequest
from utils.security import get_hash_password, verify_password


# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 创建新用户
async def create_user(db: AsyncSession, user_data: UserRegisterRequest):
    # 先密码加密处理 -> add
    hashed_secure_password = get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_secure_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # 从数据库读回最新的 user
    return user


# 生成 Token
async def create_token(db: AsyncSession, user_id: int):
    # 生成 Token + 设置过期时间 + 查询数据库当前用户是否有 Token -> 有：更新；没有：添加
    token = str(uuid.uuid4())
    # timedelta(days=7, hours=2, minutes=30, seconds=10)，可以设置更细粒度的过期时间
    expires_at = datetime.now() + timedelta(days=7)  # Token 有效期 7 天
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()

    return token


# 验证用户名和密码
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    # 验证密码
    if not verify_password(password, user.password):
        return None

    return user


# 更具 Token 查用户：验证 Token 是否有效 -> 查用户信息
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    # 验证 Token 是否存在和是否过期
    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 更新用户信息：update更新 -> 检查是否命中 -> 获取更新后的用户信息
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    # update(User).where(User.username == username).values(字段=新值, 字段=新值)
    # user_data 是一个 Pydantic 模型，得到字典 -> **解包
    # 没有设置的字段值为 None，update 语句会把数据库对应字段更新为 None，所以需要过滤掉值为 None 的字段
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    ))
    result = await db.execute(query)
    await db.commit()

    # 检查更新
    if result.rowcount == 0:
        return HTTPException(status_code=404, detail="用户不存在")

    # 返回更新后的用户信息
    updated_user = await get_user_by_username(db, username)
    return updated_user


# 修改密码：先验证旧密码 -> 新密码加密 -> 修改密码
async def change_password(db: AsyncSession, user: User, old_password: str, new_password: str):
    # 验证旧密码
    if not verify_password(old_password, user.password):
        return False

    # 新密码加密
    hashed_new_password = get_hash_password(new_password)

    # 更新密码
    user.password = hashed_new_password
    # 更新：由 SQLAlchemy 真正接管这个 User 对象，确保可以commit
    # 规避 session 过期或关闭导致的不能提交的问题
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return True


