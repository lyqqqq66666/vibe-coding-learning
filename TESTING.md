# vibe-coding-learning 端到端测试指南

> 覆盖所有 9 个模式 + 三档深度 + 状态机闭环 + 多工具兼容
> 预计耗时：30 分钟

---

## 第一步：Clone 仓库并安装

```bash
git clone https://github.com/lyqqqq66666/vibe-coding-learning.git
cd vibe-coding-learning
```

**确认文件结构**：

```bash
ls skills/vibe-coding-learning/SKILL.md   # 主入口
ls skills/vibe-coding-learning/config.yaml # 配置层
ls skills/vibe-coding-learning/references/ # 参考手册（8 个文件）
ls skills/vibe-coding-learning/scripts/    # 校验脚本（2 个）
```

**安装到你的 AI 工具**（任选一个）：

```bash
# WorkBuddy
cp -r skills/vibe-coding-learning ~/.workbuddy/skills/

# Claude Code
cp -r skills/vibe-coding-learning ~/.claude/skills/

# 其他工具参照 README 中的兼容表
```

---

## 第二步：建一个测试项目

在 repo 外面新建一个 FastAPI + SQLite 待办事项 API：

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

---

## 第三步：Mode 1 测试（学习笔记生成）

### 测试 1a：轻量模式

> "轻量模式，总结 test-project 中 main.py 的 JWT 认证"

**预期**：
- 仅输出知识点 + 卡片
- 不执行 Phase 3（陷阱）和 Phase 4（归档）的全部内容
- Token 消耗 ~2K

### 测试 1b：标准模式（Auto 直出）

> "总结 test-project 中 main.py 的 JWT 认证实现"

**预期**：
- 静默执行全流程
- 生成完整笔记 + domain 索引 + 日历 + 卡片
- 笔记 frontmatter 包含 `status: processed`

### 测试 1c：协作模式（模糊指令）

> "帮我整理学习笔记"

**预期**：
- 进入 Collaborative 模式
- 最多问 3 个问题确认范围
- 说"直接做" → 切到 Auto

### 验证产出物

```bash
# 1. 笔记是否生成
ls learning-notes/topics/
# 应有 test-project/ 或类似文件夹

# 2. domain 索引是否同步
cat learning-notes/domains/backend/_index.md
# 应包含 JWT、bcrypt、Depends 等知识点

# 3. frontmatter 检查
head -5 learning-notes/topics/*/2026-06-*.md
# 应有 ---
# status: processed
# domain: backend
# stack: fastapi
# ...

# 4. 日历是否更新
cat learning-notes/calendar/2026-06.md

# 5. 卡片是否生成
ls learning-notes/cards/auth/
# 应有 jwt.md
```

---

## 第四步：Mode 2 测试（复习召回）

> "复习昨天 JWT 的内容"

**预期**：
- 生成测验式复习卡片（不是重读笔记）
- 至少 3 个主动召回问题

---

## 第五步：Mode 3 测试（进度检查）

> "我学了多少了"

**预期**：
- 输出进度仪表盘
- mastery ratio（🟢/🟡/🔴）
- 建议补弱方向

---

## 第六步：Mode 4 测试（面试准备）

> "帮我准备后端开发面试"

**预期**：
- 进入 Collaborative，确认岗位方向
- 生成面试话术 + 模拟提问
- 参照 `references/interview-prep.md`

---

## 第七步：Mode 5 测试（提示词优化）

> "我的提示词怎么样，怎么问才能得到更好回答"

**预期**：
- 分析最近与 AI 的对话质量
- 输出提示词评分（多个维度）
- 给出"改前 vs 改后"对比
- 参考资料链接真实可访问

---

## 第八步：Mode 6 测试（收件箱整理）

> "有什么没整理的笔记吗"

**预期**：
- 扫描未处理的会话
- 建议整理方案
- 推进知识状态流转（inbox → processed）

---

## 第九步：Mode 7 测试（知识关联）

> "今天学的 JWT 和之前学的内容有什么关联"

**预期**：
- 生成新旧知识交叉引用
- 显示知识关联图
- 参照 `references/connection-review.md`

---

## 第十步：Mode 8 测试（周总结）

> "周总结，这周学了什么"

**预期**：
- 深度提炼一周学习内容
- 领域覆盖分析
- 薄弱点识别 + 下周建议

---

## 第十一步：Mode 9 测试（健康诊断）

> "检查我的学习健康度"

**预期**：
- 遗忘风险检测（N 天未复习的领域）
- 领域偏科分析
- 笔记堆积检查
- 参照 `references/health-check.md`

---

## 第十二步：不应触发测试

逐条说以下内容，验证 Skill **不触发**：

| 语句 | 预期 |
|------|------|
| "帮我在这个函数里加个 try-catch" | ❌ 不触发 |
| "review 一下我的 PR" | ❌ 不触发 |
| "帮我把变量名改成驼峰命名" | ❌ 不触发 |
| "今天天气怎么样" | ❌ 不触发 |
| "这个 bug 怎么修" | ❌ 不触发 |

---

## 第十三步：边界测试

| 语句 | 预期行为 |
|------|---------|
| "帮我看看这个代码" | Collaborative，先澄清意图 |
| "整理一下" | Collaborative，先澄清 |
| "轻量模式，总结一下" + 会话只有改了一行 CSS | light 档但建议跳过 |

---

## 第十四步：脚本验证

```bash
# 目录结构校验
python3 skills/vibe-coding-learning/scripts/validate-structure.py ./learning-notes/

# 会话复杂度分析
python3 skills/vibe-coding-learning/scripts/analyze-session.py --project ./test-project/
```

**预期**：
- `validate-structure.py`：检查 frontmatter、domain 标签、状态字段
- `analyze-session.py`：输出复杂度分数和推荐深度档位

---

## 验收单

| 检查项 | 预期 | 实际 |
|--------|------|------|
| Mode 1 轻量模式 | ✅ 知识点+卡片 | |
| Mode 1 标准模式 | ✅ 全流程+frontmatter | |
| Mode 1 协作模式 | ✅ 先确认再执行 | |
| Mode 2 复习召回 | ✅ 主动召回测验 | |
| Mode 3 进度仪表盘 | ✅ mastery ratio | |
| Mode 4 面试准备 | ✅ 话术+模拟 | |
| Mode 5 提示词优化 | ✅ 评分+改前改后 | |
| Mode 6 收件箱整理 | ✅ 未处理检测 | |
| Mode 7 知识关联 | ✅ 交叉引用 | |
| Mode 8 周总结 | ✅ 深度提炼 | |
| Mode 9 健康诊断 | ✅ 遗忘+偏科 | |
| 不应触发（5条） | ✅ 全不触发 | |
| 边界测试（3条） | ✅ 澄清后路由 | |
| validate 脚本 | ✅ frontmatter+domain | |
| analyze 脚本 | ✅ 深度推荐 | |

---

## 清理

```bash
rm -rf test-project/ test.db
rm -rf learning-notes/topics/test-project/
```
