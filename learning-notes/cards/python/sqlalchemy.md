# 知识点卡片：SQLAlchemy ORM

## 一句话定义
SQLAlchemy 是 Python 最流行的 ORM 框架，让你用 Python 类和对象来操作数据库表，而不需要手写 SQL 语句。

## 核心概念
- **ORM**（Object-Relational Mapping）：对象关系映射，把数据库表映射为 Python 类
- **Engine**：数据库连接引擎
- **Session**：数据库会话，管理事务（增删改查）
- **Base**：声明式基类，所有模型继承它
- **Model**：继承 Base 的 Python 类，对应数据库中的一张表

## Python 用法

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 创建引擎
engine = create_engine("sqlite:///./app.db")

# 2. 创建基类
Base = declarative_base()

# 3. 定义模型
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# 4. 建表
Base.metadata.create_all(bind=engine)

# 5. CRUD 操作
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# 查询
user = db.query(User).filter(User.name == "alice").first()

# 添加
db.add(User(name="bob"))
db.commit()
```

## 关键注意点
- SQLite 需要加 `connect_args={"check_same_thread": False}`
- `db.commit()` 才会真正写入数据库
- `db.refresh(user)` 在 commit 后更新对象状态
- `unique=True` 在数据库层面保证唯一性，但应在业务层先检查

## 相关文件
- `fastapi-auth/database.py`（引擎和会话配置）
- `fastapi-auth/models.py` 第 8-14 行（User 模型定义）
