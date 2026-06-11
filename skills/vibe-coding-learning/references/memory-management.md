# 记忆与知识管理策略 (Memory Management)

> 定义学习笔记的归档、组织、跨会话持久化规则。遵循 SKILL.md 的三层架构。

---

## 一、三层架构概述

```
learning-notes/
├── topics/       ← Layer 1: 原始会话笔记（按项目分文件夹）
├── domains/      ← Layer 2: 领域知识索引（按技术域组织）
└── cards/        ← Layer 3: 可复用知识点卡片（按类别分）
```

---

## 二、Layer 1 — 主题笔记 (topics/)

### 创建规则

| 条件 | 操作 |
|------|------|
| coding session 首次写入 | 创建 `topics/[project-name]/` 文件夹 |
| 同一项目追加 | 在已有文件夹下创建新的日期笔记 |
| 项目名称 | 取简短英文名，如 `fastapi-login-register`、`html-css-js-login` |

### 文件命名

```
topics/[project-name]/YYYY-MM-DD-[brief-title].md
```

例：`topics/fastapi-login-register/2026-06-11-fastapi-login-register.md`

### 内容要求
- 完整的 6 板块笔记（按 output-templates.md 规范）
- 标记关联的知识点卡片路径
- 标记关联的领域索引路径

---

## 三、Layer 2 — 领域索引 (domains/)

### 创建规则

| 条件 | 操作 |
|------|------|
| 遇到新领域 | 创建 `domains/[domain]/_index.md` |
| 遇到新栈 | 创建 `domains/[domain]/[stack]/_index.md` |
| 已存在 | 更新索引文件，追加新知识点 |

### 领域名规范

使用小写英文，对照 `knowledge-taxonomy.md`：

```
domains/
├── backend/        # 后端
│   ├── _index.md
│   ├── fastapi/
│   ├── django/
│   └── express/
├── frontend/       # 前端
│   ├── _index.md
│   ├── react/
│   ├── vue/
│   └── vanilla-js/
├── database/
├── devops/
├── ai-ml/
├── cloud/
├── security/
└── testing/
```

### _index.md 格式

```markdown
# [领域/栈名称]

## 已掌握知识点清单
- [x] 知识点 A → 关联卡片 `cards/auth/jwt.md`
- [ ] 知识点 B（待学习）

## 相关学习记录
- 2026-06-11: [FastAPI 登录注册](topics/...)
```

---

## 四、Layer 3 — 知识点卡片 (cards/)

### 创建规则

| 条件 | 操作 |
|------|------|
| 提取到新知识点 | 创建 `cards/[category]/[name].md` |
| 知识点已存在 | 在卡片末尾追加"出现项目"行 |
| 类别不存在 | 创建新类别文件夹 |

### 类别名规范（对照 SKILL.md Card Category Guidelines）

```
cards/
├── auth/        # 认证授权
├── css/         # CSS 属性/布局/动画
├── js/          # JavaScript 特性
├── ts/          # TypeScript
├── python/      # Python 及框架
├── database/    # 数据库
├── devops/      # 运维
├── ai-ml/       # AI/ML
├── security/    # 安全
└── testing/     # 测试
```

### 卡片复用规则
- 同一知识点在多项目中遇到 → 卡片追加"出现项目"行
- 不修改已有内容，只追加
- 卡片名用 kebab-case

---

## 五、进度维护 (progress.md)

### 更新时机
- 每次生成笔记后更新
- 新增领域时增加进度条
- 统计数据自动重算

### 进度条计算
- 进度 = 已打勾项 / 总清单项
- 新领域初始清单：根据 knowledge-taxonomy.md 的"知识点提取维度"生成 TODO 清单
- 每学一个标记 `[x]`

---

## 六、日历维护 (calendar/)

### 格式
```
calendar/YYYY-MM.md  → 按月分文件
```

### 追加规则
- 检查当月文件是否存在
- 追加新行到表格末尾
- 同一天多次学习 → 多行

---

## 七、重复与冲突处理

| 场景 | 处理 |
|------|------|
| 同一天同一主题再写笔记 | 追加到已有文件，不新建 |
| 知识点卡已存在 | 追加"出现项目"行 |
| 领域索引已存在 | 仅更新清单和关联 |
| 文件夹已存在 | 直接写入，不覆盖 |
| 文件名冲突 | 追加 `-2` 后缀 |
