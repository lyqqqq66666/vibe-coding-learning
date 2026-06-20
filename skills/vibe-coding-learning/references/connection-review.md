# connection-review — 知识关联

## 目的

新知识不是孤立的。每次写入新笔记后，自动检测与已有笔记的关联，构建知识网络。

## 关联类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `same_topic` | 同一主题的不同角度 | JWT 认证 vs Session 认证 |
| `prerequisite` | 前置知识 | 学 FastAPI 前应该懂 Python 装饰器 |
| `extension` | 拓展应用 | 学完 REST API 后拓展到 GraphQL |
| `contrast` | 对比辨析 | MySQL vs PostgreSQL 适用场景 |
| `example` | 同一概念的不同示例 | 用不同语言实现同一算法 |

## 触发时机

1. **写入新笔记后** — 立即执行关联检测
2. **用户主动请求** — "帮我看看今天学的和之前有什么关联"
3. **定期回顾** — Mode 3 进度报告时附带关联建议

## 检测逻辑

### 1. 关键词重叠检测

提取新笔记的 `tags` 和标题关键词，与已有笔记匹配：

```python
# 伪代码
new_tags = ["fastapi", "jwt", "auth"]
existing_notes = scan_learning_notes()

for note in existing_notes:
    overlap = len(set(new_tags) & set(note.tags))
    if overlap >= 2:
        suggest_connection(note)
```

### 2. 时间邻近检测

同一天或连续几天内学习的主题，大概率有关联：

```
2026-06-18: fastapi-basics.md
2026-06-19: jwt-auth.md          ← 时间邻近 + 主题相关 = 强关联
2026-06-20: react-components.md  ← 时间邻近但主题无关 = 弱关联
```

### 3. 知识图谱追踪

维护一个 `connections.json`：

```json
{
  "fastapi-login.md": [
    {"target": "jwt-basics.md", "type": "prerequisite", "strength": 0.9},
    {"target": "python-decorators.md", "type": "prerequisite", "strength": 0.8}
  ]
}
```

## 输出格式

```markdown
## 知识关联建议

### 强关联（建议立即建立链接）
- `fastapi-login.md` ↔ `jwt-basics.md`
  - 关联类型：前置知识
  - 理由：登录流程依赖 JWT 原理
  - 建议操作：在两篇笔记中都添加 `[[双向链接]]`

### 弱关联（可选建立链接）
- `fastapi-login.md` ↔ `sqlalchemy-orm.md`
  - 关联类型：同一项目不同层
  - 理由：登录后通常需要查询用户表

### 对比关联（建议生成对比笔记）
- `session-auth.md` vs `jwt-auth.md`
  - 建议：创建 `auth-comparison.md` 对比两种方案
```

## 双向链接格式

在笔记中用小括号双向链接：

```markdown
## 相关笔记
- [[jwt-basics|JWT 基础]] — 登录依赖的认证原理
- [[python-decorators|Python 装饰器]] — FastAPI 路由依赖此语法
```

## 自动化建议

当检测到强关联时，AI 可以自动在笔记中插入链接（需用户确认）：

```markdown
💡 检测到新笔记 `fastapi-login.md` 与已有笔记存在强关联，
   要我自动在两边插入双向链接吗？
```
