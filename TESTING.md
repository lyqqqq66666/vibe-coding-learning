# vibe-coding-learning 端到端测试脚本

> 给 Claude（或其他 AI 工具）用的测试剧本。跟着步骤走，每一步可独立验证。
> 预计耗时：15 分钟。

---

## 第一步：Clone 仓库

```bash
git clone https://github.com/lyqqqq66666/vibe-coding-learning.git
cd vibe-coding-learning
```

确认文件结构：

```bash
ls skills/vibe-coding-learning/SKILL.md   # 应该有
ls AGENTS.md                              # 应该有
ls learning-notes/                        # 应该为空或只有已有数据
```

---

## 第二步：建一个测试项目

在当前目录下新建一个 FastAPI + SQLite 待办事项 API。要求：

### 创建以下文件

**`test-project/main.py`**
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from pydantic import BaseModel
import jwt
import bcrypt
import os

app = FastAPI()
security = HTTPBearer()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

SECRET_KEY = os.urandom(32).hex()
ALGORITHM = "HS256"

class TodoModel(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    done = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

class TodoCreate(BaseModel):
    title: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/login")
def login(username: str, password: str):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    token = jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}

@app.post("/todos")
def create_todo(todo: TodoCreate, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_todo = TodoModel(title=todo.title)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos")
def list_todos(user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(TodoModel).all()
```

**`test-project/requirements.txt`**
```
fastapi
uvicorn
sqlalchemy
pyjwt
bcrypt
```

安装依赖并启动验证：

```bash
cd test-project
pip install -r requirements.txt
python main.py   # 应该能启动，Ctrl+C 退出即可
```

---

## 第三步：触发 Skill Mode 1（模糊指令 → 验证双模式）

**把 SKILL.md 发给 Claude 作为指令**（或直接在当前 repo 中让 AI 读取 `skills/vibe-coding-learning/SKILL.md`），然后说：

> "帮我总结今天学的"

**预期行为（Collaborative 模式）**：
- AI 应该先确认，而不是直接执行
- 最多问 3 个问题，比如"聚焦哪些文件？""侧重哪个方向？"
- 说出"直接做" → 应该切到 Auto 模式，不再追问

---

## 第四步：触发 Skill Mode 1（精确指令 → 验证 Auto 直出）

> "总结 test-project 中 main.py 的 JWT 认证实现"

**预期行为（Auto 模式）**：
- AI 应该静默执行，不再提问
- 如果执行较慢（> 5 秒），应出现 Phase 1/5... 的进度提示
- 如果很快完成，跳过进度提示

---

## 第五步：检查产出物

### 检查 1 — 学习笔记是否生成

```bash
ls learning-notes/topics/
# 应该有一个 test-project/ 或类似文件夹
ls learning-notes/topics/*/2026-06-11*.md
```

打开笔记文件，确认包含：
- 知识点提取（JWT、bcrypt、SQLAlchemy、FastAPI Depends 等）
- 代码逐段讲解
- 易错点整理

### 检查 2 — domains/ 索引是否同步

```bash
ls learning-notes/domains/backend/
# 应该有 _index.md
cat learning-notes/domains/backend/_index.md
# 内容应包含本次的知识点清单
```

### 检查 3 — 日历是否更新

```bash
cat learning-notes/calendar/2026-06.md
# 应有今天日期的条目
```

### 检查 4 — 进度文件是否更新

```bash
cat learning-notes/progress.md
# 应有三级 mastery 标记：🟢 熟练 / 🟡 理解 / 🔴 接触
```

### 检查 5 — 知识卡片是否生成

```bash
ls learning-notes/cards/
# 应有 auth/ 或 python/ 等分类文件夹，内含 jwt.md 等卡片
```

### 检查 6 — WebSearch 行为

查看笔记中的"推荐资源"部分：
- 如果有搜索能力 → 应有具体的 B 站/文档链接
- 如果没有搜索能力 → 应标注"（基于通用知识推荐，非实时搜索结果）"，且没有编造的 URL

---

## 第六步：测试 Mode 3（进度检查）

> "看看我的学习进度"

**预期**：展示领域进度、mastery ratio（熟练数/总数 × 100%）、学习日历、建议补弱方向。

---

## 验收单

| 检查项 | 预期 | 实际 |
|--------|------|------|
| 模糊指令 → 先确认再执行 | ✅ Collaborative |  |
| 精确指令 → 直接出结果 | ✅ Auto |  |
| topics/ 生成笔记 | ✅ |  |
| domains/ 索引同步 | ✅ |  |
| 日历更新 | ✅ |  |
| progress.md 三级 mastery | ✅ |  |
| cards/ 生成卡片 | ✅ |  |
| WebSearch 行为正确 | ✅ 有链接或标注 |  |
| Mode 3 进度总览 | ✅ |  |

---

## 清理（可选）

```bash
cd /path/to/vibe-coding-learning
rm -rf test-project/ test.db learning-notes/topics/test-project/
```
