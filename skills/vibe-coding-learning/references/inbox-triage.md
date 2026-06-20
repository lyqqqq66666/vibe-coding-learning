# inbox-triage — 知识生命周期管理

## 核心概念

笔记不是"写完了事"，而是有生命的循环：

```
原始会话笔记
    ↓
[待处理] inbox
    ↓ （用户确认/AI 自动分类）
[已整理] processed
    ↓ （AI 检测关联）
[已关联] connected
    ↓ （用户标记为掌握）
[已掌握] mastered
```

## 状态定义

| 状态 | 含义 | 后续动作 |
|------|------|----------|
| `inbox` | 刚从对话提取，未分类 | 需要用户确认领域/主题 |
| `processed` | 已分类归档到对应目录 | 等待关联检测 |
| `connected` | 已与其他笔记建立关联 | 等待用户复习 |
| `mastered` | 用户标记为已掌握 | 从主动复习列表中移除 |

## 工作流程

### Step 1：检测 inbox

扫描 `learning-notes/` 目录，找出：
- 文件名含 `temp_` 或 `session_` 的未整理笔记
- 最近 3 天内创建但未移动的笔记
- `inbox/` 子目录下的所有笔记

### Step 2：批处理分类

```
请用户确认：
"发现 3 条未整理的会话笔记：
 1. [2026-06-18-fastapi-login] → 建议归档到 backend/api/
 2. [2026-06-19-react-hooks] → 建议归档到 frontend/hooks/
 3. [2026-06-20-docker-compose] → 建议归档到 devops/container/

确认移动？或修改分类？"
```

### Step 3：关联检测

对刚分类的笔记，搜索同领域其他笔记，建议关联：

```markdown
## 建议关联
- `backend/api/fastapi-login.md` 与 `backend/auth/jwt-basics.md` 主题相似
- 建议添加双向链接：[[jwt-basics]]
```

### Step 4：晋升检查

当用户多次复习某笔记后，提示晋升：

```markdown
💡 你在过去 2 周内复习了 `fastapi-login.md` 3 次，
   看起来已经掌握了。要标记为「已掌握」吗？
```

## 触发方式

```
用户说：
- "有什么没整理的笔记吗"
- "整理一下 inbox"
- "批处理今天的会话"
- "检查笔记状态"
```

## 输出格式

```markdown
# Inbox Triage 报告

## 待处理（3 条）
- [ ] `temp_session_20260618.md` — FastAPI 登录
- [ ] `temp_session_20260619.md` — React Hooks
- [ ] `temp_session_20260620.md` — Docker Compose

## 已整理待关联（2 条）
- [ ] `backend/api/fastapi-login.md` — 建议关联：`../auth/jwt-basics.md`
- [ ] `frontend/hooks/useEffect.md` — 建议关联：`../react/lifecycle.md`

## 可晋升为「已掌握」（1 条）
- [x] `backend/auth/jwt-basics.md` — 已复习 3 次
```
