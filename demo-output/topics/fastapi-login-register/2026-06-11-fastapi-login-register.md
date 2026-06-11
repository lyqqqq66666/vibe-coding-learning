# FastAPI 登录注册后端 — 学习笔记

> 日期：2026-06-11
> 技术领域：后端开发 / Web 安全 / 用户认证
> 项目：`fastapi-auth/`

---

## 一、本次做了什么

用 FastAPI + SQLAlchemy + SQLite + JWT 实现了一个完整的用户登录注册后端，包含 3 个 API 接口：

| 接口 | 功能 |
|------|------|
| `POST /register` | 用户注册（用户名 + 邮箱 + 密码） |
| `POST /login` | 用户登录，返回 JWT Token |
| `GET /me` | 获取当前登录用户信息（需 Token） |

项目共 5 个源文件，结构清晰：

```
fastapi-auth/
├── main.py          ← 应用入口 + CORS 配置
├── database.py      ← 数据库连接 + 会话管理
├── models.py        ← 数据库模型 + Pydantic 请求/响应模型
├── auth.py          ← 密码哈希 + JWT 生成/验证 + 用户认证
└── routes.py        ← API 路由（注册/登录/获取用户）
```

---

## 二、知识点提取

### 知识点 1：FastAPI 框架基础

**定义**：FastAPI 是一个高性能的 Python Web 框架，基于 Starlette 和 Pydantic 构建，自带 API 文档和类型校验。

**核心概念**：
- 使用 `FastAPI()` 创建应用实例
- 用装饰器 `@app.get()` / `@app.post()` 定义路由
- 用 `APIRouter()` 实现模块化路由拆分
- `app.include_router(router)` 将路由挂载到应用

**对应代码**：`main.py` 第 6-18 行

**阅读顺序**：先看 `main.py`，理解应用如何启动和挂载路由。

---

### 知识点 2：Pydantic 数据模型与请求校验

**定义**：Pydantic 是 Python 的数据验证库，FastAPI 用它来定义请求体的结构和自动校验。

**核心概念**：
- `BaseModel` 定义请求/响应的数据结构
- `EmailStr` 自动校验邮箱格式（需要 `pydantic[email]`）
- `model_config = {"from_attributes": True}` 允许从 ORM 对象转 Pydantic 模型
- FastAPI 自动根据 Pydantic 模型生成 Swagger 文档

**对应代码**：`models.py` 第 19-40 行

**阅读顺序**：看完 `main.py` 后读 `models.py`，理解数据如何在不同层之间流转。

---

### 知识点 3：SQLAlchemy ORM 与数据库操作

**定义**：SQLAlchemy 是 Python 最流行的 ORM（对象关系映射）框架，让你用 Python 类操作数据库表，而不需要写 SQL 语句。

**核心概念**：
- `create_engine()` 创建数据库引擎
- `declarative_base()` 创建基类，所有模型继承它
- `Column()` 定义表的列（类型、主键、唯一约束、索引）
- `SessionLocal()` 创建数据库会话
- `get_db()` 是一个生成器（`yield`），用 `Depends()` 注入到路由函数
- `Base.metadata.create_all()` 自动建表

**对应代码**：`database.py` 全文，`models.py` 第 8-14 行

**阅读顺序**：先看 `database.py` 理解数据库连接方式，再看 `models.py` 的 `User` 类。

---

### 知识点 4：bcrypt 密码哈希

**定义**：bcrypt 是一种专门用于密码存储的哈希算法，基于 Blowfish 加密算法，自带"盐"（salt）和可调节的计算成本，能有效抵御暴力破解和彩虹表攻击。

**核心概念**：
- **永远不要明文存储密码**，数据库里只存哈希值
- `bcrypt.hashpw(password, salt)` 生成哈希
- `bcrypt.gensalt()` 自动生成随机盐
- `bcrypt.checkpw(plain, hashed)` 验证密码是否匹配
- bcrypt 是单向函数，无法从哈希值反推出原始密码
- 输入输出需要 `bytes` 类型，所以要用 `.encode("utf-8")` 和 `.decode("utf-8")`

**对应代码**：`auth.py` 第 26-33 行

**阅读顺序**：在理解注册流程时重点看 `hash_password()` 和 `verify_password()`。

---

### 知识点 5：JWT（JSON Web Token）认证

**定义**：JWT 是一种无状态的认证机制，服务端不需要存储 Session，而是签发一个包含用户信息的加密 Token，客户端每次请求都携带这个 Token。

**核心概念**：
- JWT 由三部分组成：`Header.Payload.Signature`，用 `.` 分隔
- `jwt.encode(payload, secret, algorithm)` 生成 Token
- `jwt.decode(token, secret, algorithms)` 解析验证 Token
- `payload` 中通常包含 `sub`（用户标识）和 `exp`（过期时间）
- `SECRET_KEY` 是签名密钥，泄露则整个认证体系失效
- Token 通过 HTTP Header `Authorization: Bearer <token>` 传递

**对应代码**：`auth.py` 第 36-41 行（生成），第 44-62 行（验证）

**阅读顺序**：先看 `create_access_token()` 理解生成过程，再看 `get_current_user()` 理解验证流程。

---

### 知识点 6：FastAPI 依赖注入（Depends）

**定义**：FastAPI 的 `Depends()` 机制允许你声明函数的"依赖"，框架会在调用函数前自动执行这些依赖，并将结果传入函数参数。

**核心概念**：
- `Depends(get_db)` 自动获取数据库会话，请求结束后自动关闭
- `Depends(get_current_user)` 自动从 Token 中解析当前用户
- `Depends(oauth2_scheme)` 自动从请求头提取 Bearer Token
- 依赖可以嵌套：`get_current_user` 依赖 `oauth2_scheme` 和 `get_db`
- 这是 FastAPI 最强大的特性之一，实现代码复用和关注点分离

**对应代码**：`routes.py` 第 18、44、59 行，`auth.py` 第 44 行

**阅读顺序**：在理解所有单独功能后，最后看 `Depends` 如何把它们串联起来。

---

### 知识点 7：CORS 跨域配置

**定义**：CORS（Cross-Origin Resource Sharing）是浏览器的安全机制，限制网页从一个域向另一个域发请求。开发前后端分离项目时，后端需要配置 CORS 允许前端跨域访问。

**核心概念**：
- `CORSMiddleware` 是 FastAPI 内置的跨域中间件
- `allow_origins=["*"]` 允许所有来源（仅开发环境使用）
- 生产环境应指定具体的前端域名

**对应代码**：`main.py` 第 9-15 行

---

## 三、代码阅读指南

推荐的阅读顺序：

1. **`main.py`** — 理解应用入口、CORS 配置、路由挂载
2. **`database.py`** — 理解数据库连接和会话管理
3. **`models.py`** — 理解数据库模型（User 表）和 Pydantic 模型（请求/响应）
4. **`auth.py`** — 理解密码哈希、JWT 生成/验证、用户认证依赖
5. **`routes.py`** — 理解 API 路由如何组合以上所有模块

核心数据流：

```
用户请求 → Pydantic 校验 → 路由函数 → Depends 注入（DB + 认证）→ 业务逻辑 → 响应
```

---

## 四、常见陷阱

| 陷阱 | 正确做法 | 常见错误 |
|------|----------|----------|
| 明文存储密码 | 用 bcrypt 哈希后存储 | 直接把用户密码写入数据库 |
| passlib 与 bcrypt 版本不兼容 | 直接用 `import bcrypt` 调用 `hashpw/checkpw` | 用 `passlib.context.CryptContext` 配合新版 bcrypt |
| JWT Secret Key 写死在代码里 | 用环境变量 `os.getenv("SECRET_KEY")` | 硬编码 `"your-secret-key"` |
| 忘记设置 Token 过期时间 | 在 payload 中加入 `exp` 字段 | 生成永不过期的 Token |
| SQLite 多线程报错 | `connect_args={"check_same_thread": False}` | 不加此参数导致多请求时报错 |
| 注册时不检查重复 | 先查询用户名/邮箱是否已存在 | 直接插入导致唯一约束报错（500 错误） |
| 返回用户信息时泄露密码 | 用 `UserResponse` 模型排除密码字段 | 直接返回包含 `hashed_password` 的 User 对象 |

---

## 五、推荐学习资源

1. **FastAPI 官方文档 — 安全与认证**
   FastAPI 官方教程中关于 OAuth2 + JWT 的完整示例，非常权威
   https://fastapi.tiangolo.com/tutorial/security/

2. **FastAPI OAuth2PasswordBearer 详解**
   详细解释了 FastAPI 中 OAuth2 密码流的工作原理
   https://blog.csdn.net/k_genius/article/details/132421404

3. **Python Web 开发实战 — JWT 实现登录与权限控制**
   从零讲解 JWT 在 Python Web 中的应用，适合入门
   https://blog.csdn.net/JENREY/article/details/128728619

4. **使用 bcrypt 进行安全密码哈希与验证**
   详解 bcrypt 的原理和 Python 中的用法
   https://blog.csdn.net/Leon_Jinhai_Sun/article/details/146120672

---

## 六、今日总结

今天通过一个 FastAPI 登录注册项目，实践了后端用户认证的完整流程：

1. **数据库建模** — 用 SQLAlchemy ORM 定义 User 表
2. **密码安全** — 用 bcrypt 对密码进行哈希存储
3. **Token 认证** — 用 JWT 实现无状态的用户认证
4. **依赖注入** — 用 FastAPI 的 `Depends` 机制优雅地管理数据库会话和用户认证
5. **模块化设计** — 将数据库、模型、认证、路由拆分为独立文件

**下一步建议**：
- 尝试添加"修改密码"和"删除账号"接口
- 将 SQLite 换成 PostgreSQL 或 MySQL
- 用环境变量管理 `SECRET_KEY`
- 添加单元测试
