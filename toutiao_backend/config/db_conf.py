from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# 数据库连接字符串，格式为：数据库类型+数据库驱动名称://用户名:密码@主机地址:端口/数据库名称
ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost:5432/postgres"

# 创建异步数据库引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 启用 SQLAlchemy 的日志输出，方便调试
    pool_size=10,  # 连接池的大小，表示同时可以保持的数据库连接数量
    max_overflow=20,  # 连接池的最大溢出数量，表示在连接池满时可以创建的额外连接数量
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定使用异步会话类
    expire_on_commit=False  # 提交后不自动过期对象，这样在提交后仍然可以访问对象的属性，而不会引发 DetachedInstanceError 错误
)


# 依赖项：获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:  # 获取数据库会话
        try:
            yield session   # 使用 yield 关键字将数据库会话作为生成器返回，这样在使用完数据库会话后，控制权会返回到这里，可以在 finally 块中关闭会话
            await session.commit()  # 提交事务
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()



