# AI 掘金头条新闻系统

一个前后端分离的新闻系统示例项目，包含用户认证、新闻浏览、收藏与历史记录等完整业务流程。

## 项目概览

- 后端：基于 FastAPI + SQLAlchemy(Async) + PostgreSQL + Redis
- 前端：基于 Vue 3 + Vite + Vant + Pinia
- 数据库脚本：根目录 `database.sql`
- 接口文档：根目录 `API接口规范文档.md`
- 后端设计说明：根目录 `项目后端设计说明文档.md`

## 核心功能

- 用户：注册、登录、获取信息、更新资料、修改密码
- 新闻：分类列表、新闻列表（分页）、新闻详情、相关新闻
- 收藏：检查状态、添加、取消、列表、清空
- 历史：添加、列表、删除单条、清空
- 缓存：新闻分类与列表缓存（Redis）

## 目录结构

```text
toutiao/
├─ toutiao_backend/               # FastAPI 后端
│  ├─ main.py                     # 应用入口（app）
│  ├─ config/                     # 数据库/Redis 配置
│  ├─ routers/                    # 路由层（news/user/favorite/history）
│  ├─ crud/                       # 数据访问层
│  ├─ models/                     # SQLAlchemy 模型
│  ├─ schemas/                    # Pydantic 请求/响应模型
│  ├─ utils/                      # 认证、响应封装、异常处理等
│  ├─ cache/                      # 缓存键与缓存逻辑
│  └─ test_main.http              # 接口调试示例
├─ toutiao_frontend/              # Vue 前端
├─ database.sql                   # 建表与示例数据
├─ API接口规范文档.md
└─ 项目后端设计说明文档.md
```

## 运行环境

- Python 3.10+（建议）
- Node.js 18+（建议）
- PostgreSQL 14+（建议）
- Redis 6+（建议）

## 快速开始

### 1) 数据库初始化

1. 创建 PostgreSQL 数据库（例如 `postgres`）。
2. 导入根目录 `database.sql`。
3. 确认已生成以下核心表：`user`、`user_token`、`news_category`、`news`、`favorite`、`history` 等。

### 2) 启动后端

进入后端目录：

```bash
cd toutiao_backend
```

安装依赖（项目当前未提供 `requirements.txt`，可先按实际导入安装）：

```bash
pip install fastapi uvicorn sqlalchemy asyncpg redis pydantic "passlib[bcrypt]"
```

启动服务：

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

启动后可访问：

- 根路由：[http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- OpenAPI 文档：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3) 启动前端

进入前端目录：

```bash
cd toutiao_frontend
```

安装依赖并启动：

```bash
npm install
npm run dev
```

构建与预览：

```bash
npm run build
npm run preview
```

## 配置说明

### 后端数据库配置

文件：`toutiao_backend/config/db_conf.py`

默认连接串示例：

```python
ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost:5432/postgres"
```

### Redis 配置

文件：`toutiao_backend/config/redis_conf.py`

默认配置：

```python
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
```

## 认证与响应规范

### 认证方式

- 登录/注册后返回 token。
- 受保护接口在请求头中传 `Authorization`。
- 后端兼容 `Bearer <token>` 形式。

示例：

```http
Authorization: Bearer your_token_here
```

### 统一响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

## 主要接口

### 用户模块（`/api/user`）

- `POST /register` 注册
- `POST /login` 登录
- `GET /info` 获取用户信息
- `PUT /update` 更新资料
- `PUT /password` 修改密码

### 新闻模块（`/api/news`）

- `GET /categories` 分类列表
- `GET /list` 新闻列表（`categoryId`、`page`、`pageSize`）
- `GET /detail` 新闻详情（`id`）

### 收藏模块（`/api/favorite`）

- `GET /check`
- `POST /add`
- `DELETE /remove`
- `GET /list`
- `DELETE /clear`

### 历史模块（`/api/history`）

- `POST /add`
- `GET /list`
- `DELETE /delete/{history_id}`
- `DELETE /clear`

更详细的请求参数与返回示例请查看 `API接口规范文档.md`。

## 开发建议

- 当前数据库与 Redis 配置为硬编码，建议改为环境变量（`.env`）。
- 建议补充 `requirements.txt` 或 `pyproject.toml`，方便环境复现。
- 建议新增自动化测试（`pytest`）与 CI 流程。

## 常见问题

- 后端无法连接数据库：检查 `db_conf.py` 的连接串、PostgreSQL 用户密码与端口。
- 缓存不生效：确认 Redis 已启动，且 `redis_conf.py` 配置正确。
- 前端请求失败：确认后端已启动在 `127.0.0.1:8000`，并检查浏览器网络请求详情。

## 调试入口

- 后端接口调试示例：`toutiao_backend/test_main.http`
- 接口文档（手写版）：`API接口规范文档.md`

