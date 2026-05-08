from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import news, users, favorite, history
from utils.exception_handlers import register_exception_handlers

app = FastAPI()


# 注册异常处理器
register_exception_handlers(app)


# 配置 CORS 中间件，允许跨域请求
origins = [
    "http://localhost:3000",
    "http://localhost"
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发可以使用，生产环境不可以
    # allow_origins=origins,  # 允许的来源列表
    allow_credentials=True,  # 允许携带凭证（如 cookies）
    allow_methods=["*"],  # 允许的 请求 方法
    allow_headers=["*"],  # 允许的 请求 头
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 注册路由/挂载路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
