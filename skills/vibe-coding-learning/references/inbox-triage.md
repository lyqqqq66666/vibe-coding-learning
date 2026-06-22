# inbox-triage — 知识生命周期管理

## 核心概念

笔记不是"写完了事"，而是有生命的循环：

```
原始会话笔记
    ↓
[待处理] inbox      ← 仅限：非 M1 创建的笔记、手动创建的笔记
    ↓ （M1 Step 2 已分类 → 自动跳到 processed）
[已整理] processed   ← M1 Step 8 保存后自动到达此状态
    ↓ （connection-review 检测关联）
[已关联] connected
    ↓ （用户标记为掌握）
[已掌握] mastered
```

## 状态定义

| 状态 | 含义 | 到达方式 |
|------|------|----------|
| `inbox` | 刚提取，未分类 | 非 M1 流程创建的笔记 |
| `processed` | 已分类归档到对应目录 | M1 Step 8 保存后自动设置 |
| `connected` | 已与其他笔记建立关联 | connection-review 执行后设置 |
| `mastered` | 用户标记为已掌握 | 用户在复习时手动标记 |

## 自动状态转换规则（重要）

| 转换 | 触发条件 | 是否需用户确认 |
|-------|----------|------------------|
| `inbox` → `processed` | M1 Step 8 保存笔记时 | ❌ 自动，无需确认 |
| `processed` → `connected` | connection-review 执行后 | ❌ 自动，提示用户确认关联 |
| `connected` → `mastered` | 用户主动标记 | ✅ 需用户确认 |

> **为什么 M1 创建的笔记跳过 inbox？**
> M1 Step 2 已经识别了 domain/stack，Step 8 按三层架构保存，
> 分类已完成，无需再走 inbox 待确认流程。

## 工作流程（仅针对非 M1 创建的笔记）

### Step 1：检测 inbox

扫描 `learning-notes/` 目录，找出：
- 文件无 YAML frontmatter 的 `status:` 字段
- 或 `status: inbox` 的笔记
- 或文件名含 `temp_` / `session_` 的未整理笔记

### Step 2：批处理分类

```
请用户确认：
"发现 3 条未整理的会话笔记：
 1. [2026-06-18-fastapi-login] → 建议归档到 backend/api/
 2. [2026-06-19-react-hooks] → 建议归档到 frontend/hooks/
 3. [2026-06-20-docker-compose] → 建议归档到 devops/container/

确认移动？或修改分类？"
```

确认后，更新文件 frontmatter `status: processed`。

### Step 3：关联检测（自动）

对刚分类的笔记，搜索同领域其他笔记，建议关联：

```markdown
## 建议关联
- `backend/api/fastapi-login.md` 与 `backend/auth/jwt-basics.md` 主题相似
- 建议添加双向链接：[[jwt-basics]]
```

用户确认后，更新 `status: connected`。

### Step 4：晋升检查

当用户多次复习某笔记后，提示晋升：

```markdown
💡 你在过去 2 周内复习了 `fastapi-login.md` 3 次，
   看起来已经掌握了。要标记为「已掌握」吗？
```

确认后，更新 `status: mastered`。

## 笔记 Frontmatter 规范

每个笔记文件头部应包含 YAML frontmatter：

```markdown
---
title: "FastAPI Login Implementation"
date: 2026-06-18
domain: backend
stack: fastapi
status: processed          # inbox / processed / connected / mastered
last_review_date: null     # YYYY-MM-DD 或 null
review_count: 0
mastery_level: "🟡 understood"   # 🟢🟢 teachable / 🟢 mastered / 🟡 understood / 🔴 exposed
tags: [auth, jwt, login]
---

# 正文开始...
```

## 触发方式

```
用户说：
- "有什么没整理的笔记吗"   → 触发 Step 1-2
- "整理一下 inbox"           → 触发 Step 1-2
- "检查笔记关联"            → 触发 Step 3
- "我哪些笔记可以标记为掌握"  → 触发 Step 4
```

## 输出格式

```markdown
# Inbox Triage 报告

## 待处理（3 条）
- [ ] `temp_session_20260618.md` — FastAPI 登录 → 建议：backend/api/
- [ ] `temp_session_20260619.md` — React Hooks → 建议：frontend/hooks/
- [ ] `temp_session_20260620.md` — Docker Compose → 建议：devops/container/

## 已整理待关联（2 条）
- [ ] `backend/api/fastapi-login.md` — 建议关联：`../auth/jwt-basics.md`
- [ ] `frontend/hooks/useEffect.md` — 建议关联：`../react/lifecycle.md`

## 可晋升为「已掌握」（1 条）
- [x] `backend/auth/jwt-basics.md` — 已复习 3 次
```
