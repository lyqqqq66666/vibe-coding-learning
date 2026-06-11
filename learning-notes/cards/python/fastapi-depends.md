# 知识点卡片：FastAPI 依赖注入（Depends）

## 一句话定义
FastAPI 的 `Depends()` 机制让你声明函数的"前置依赖"，框架在调用路由函数前自动执行这些依赖，并将结果传入函数参数。

## 核心概念
- **依赖注入**（Dependency Injection）是一种设计模式，将组件的创建和管理交给框架
- FastAPI 用 `Depends(依赖函数)` 声明依赖
- 依赖可以嵌套：A 依赖 B，B 依赖 C，框架自动按顺序解析
- 依赖函数可以是生成器（`yield`），框架在请求结束后自动执行清理逻辑

## 常见用法

```python
# 1. 数据库会话注入
@router.post("/register")
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    ...

# 2. 用户认证注入
@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    ...

# 3. 嵌套依赖
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    ...
```

## 为什么重要
- **代码复用**：多个路由共享同一个认证逻辑，不需要重复写
- **关注点分离**：每个依赖函数只做一件事
- **自动清理**：生成器依赖的 `finally` 块确保资源释放

## 相关文件
- `fastapi-auth/database.py` 第 13-18 行（get_db 生成器）
- `fastapi-auth/auth.py` 第 44 行（get_current_user 嵌套依赖）
- `fastapi-auth/routes.py` 第 18、44、59 行（路由中使用 Depends）
