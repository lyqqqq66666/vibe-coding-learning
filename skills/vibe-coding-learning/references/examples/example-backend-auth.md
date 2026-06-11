# 示例：后端认证 — FastAPI + JWT 学习笔记

> 这是 `vibe-coding-learning` Skill 生成的完整示例输出。展示了 Mode 1 的标准产出质量。

---

## 基本信息

- **日期**：2026-06-11
- **技术领域**：后端开发 / 认证与安全
- **AI 工具**：WorkBuddy
- **任务描述**：用 FastAPI + SQLAlchemy + JWT 实现了用户登录注册后端

---

## 知识点归纳

### 1. JWT 认证机制

- **是什么**：JSON Web Token，一种无状态的认证方式
- **核心原理**：用户登录后服务端签发 Token，客户端存储并在每次请求时携带，服务端验证签名和有效期
- **关键代码**：`auth.py` 第 36-62 行

### 2. bcrypt 密码哈希

- **是什么**：基于 Blowfish 的密码专用哈希算法，自带加盐和抗暴力破解
- **核心原理**：加盐 + 多轮迭代，无法从哈希值反推原文
- **关键代码**：`auth.py` 第 26-33 行

### 3. FastAPI 依赖注入（Depends）

- **是什么**：FastAPI 声明式依赖管理机制，自动执行依赖函数并注入结果
- **核心原理**：通过 `Depends()` 声明函数依赖，框架在调用路由前自动解析和执行
- **关键代码**：`routes.py` 第 18、44、59 行

---

## 代码讲解

### 先读哪里

建议阅读顺序：`main.py` → `database.py` → `models.py` → `auth.py` → `routes.py`

### 逐段解读

#### main.py — 应用入口

```python
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.include_router(router)
```

- 创建 FastAPI 实例
- 添加 CORS 中间件支持跨域
- 挂载路由模块

#### auth.py — 认证核心

```python
def create_access_token(data: dict):
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user = db.query(User).filter_by(id=payload["sub"]).first()
    return user
```

- `create_access_token`：将用户信息编码为 JWT
- `get_current_user`：从请求头提取 Token → 解码 → 查数据库 → 返回用户对象
- 错误处理：Token 过期/无效分别返回不同错误信息

### 为什么这样设计

- **为什么用 JWT？** 无状态，不需要服务端存 Session，方便水平扩展和多端接入
- **为什么用 bcrypt？** 自带盐值和可调节计算成本，专门对抗暴力破解和彩虹表
- **为什么分成 5 个文件？** 关注点分离：入口/数据库/模型/认证/路由各自独立

---

## 易错点整理

| 易错点 | 正确做法 | 常见错误 |
|--------|---------|---------|
| 明文存储密码 | bcrypt 哈希后存储 | 把用户密码直接写入数据库 |
| SECRET_KEY 硬编码 | `os.getenv("SECRET_KEY")` | `"your-secret-key"` |
| 忘记 Token 过期 | payload 加 `exp` 字段 | 永不过期的 Token |
| SQLite 多线程报错 | `check_same_thread=False` | 不加导致并发请求崩溃 |
| 返回用户信息泄露密码 | 用 Response Model 排除 | 直接返回 User 对象 |

---

## 推荐学习资源

1. **[文档] FastAPI 官方 — Security**
   官方 OAuth2 + JWT 教程，最权威
   https://fastapi.tiangolo.com/tutorial/security/

2. **[B站] Python Web 开发 — JWT 登录与权限**
   从零讲解 JWT 在 Python Web 中的应用
   搜索关键词：FastAPI JWT 认证 实战

3. **[博客] bcrypt 密码哈希详解**
   详解 bcrypt 原理和 Python 用法
   https://blog.csdn.net/Leon_Jinhai_Sun/article/details/146120672

---

## 下一步学习建议

- [ ] 添加 Refresh Token 机制
- [ ] 实现 RBAC 角色权限控制
- [ ] 学习 Alembic 数据库迁移
