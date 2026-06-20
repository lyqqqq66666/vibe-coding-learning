# Vibe Coding Learning — Web 端原型设计文档

> 给 Codex 阅读，用于制作网页端原型
> 作者：lyqqqq66666 | 项目：vibe-coding-learning Skill 参赛作品

---

## 一、项目背景

### 1.1 核心痛点

目前使用 AI 编程工具（WorkBuddy、Claude Code、OpenClaw、Trae、Codex 等）的用户面临一个问题：

- 每个 AI 工具各自保存对话记录，散落在不同隐藏目录（`~/.workbuddy/`、`~/.claude/`、`~/.openclaw/`、`~/.trae-cn/`、`~/.codex/`）  
- 用户在一个项目里可能同时用了多个 AI 工具，但无法统一回顾"我在这个项目里和 AI 一起学了什么"
- 原有 `vibe-coding-learning` Skill 只能在单个 AI 工具内触发，无法跨工具聚合

### 1.2 解决方案

做一个**网页端 Vibe Coding Learning Hub**，核心能力：

1. **聚合**：导入本地项目文件夹，自动识别其中包含的各 AI 工具对话记录，统一展示
2. **同步**：本地项目文件更新后，网页端可同步更新
3. **分析**：新增 Skill 功能，分析用户与 AI 的对话，提炼学习洞察，并指导用户优化提示词
4. **知识化**：借鉴 NotebookLM + Obsidian 的笔记方法，把 AI 对话转化为结构化学习笔记

### 1.3 参赛背景

本文档对应的作品将参加 **腾讯云 AI Agent 钳王争霸征文比赛**（征稿截止 2026.6.30），投稿至腾讯云开发者社区。

---

## 二、核心功能清单

### F1：项目文件夹导入

| 子功能 | 说明 |
|--------|------|
| 手动导入 | 用户选择本地项目文件夹路径，网页端读取其中的 AI 对话数据 |
| 自动识别 | 扫描文件夹，自动识别包含哪些 AI 工具的目录（`.workbuddy/`、`/.claude/`、`.openclaw/`、`/.trae-cn/`、`.codex/` 等） |
| 权限提示 | 首次访问本地文件时，明确告知用户将读取哪些目录，获得确认后才执行 |

**安全设计**：
- 只读取已知的 AI 工具目录，不访问项目外的文件
- 可选"仅导入模式"，上传后本地不再保留访问权限
- 界面上始终显示"当前正在读取：xxx 目录"，透明可控

---

### F2：多 AI 对话聚合展示

| 子功能 | 说明 |
|--------|------|
| 按项目聚合（默认） | 同一项目的所有 AI 对话合并展示，时间线排序 |
| 按 AI 工具分类（可选） | 左侧可切换"按项目视图" / "按 AI 工具视图" |
| 对话内容解析 | 提取对话中的代码片段、决策理由、错误修复记录 |

**数据来源示例**：
```
my-project/
├── .workbuddy/          ← WorkBuddy 对话记录
├── .claude/             ← Claude Code 对话记录
├── .openclaw/           ← OpenClaw 对话记录
├── .trae-cn/            ← Trae 对话记录（或项目内 .trae/）
├── .codex/              ← Codex 对话记录
└── src/                  ← 项目代码（用于关联对话上下文）
```

---

### F3：与 Skill 集成（新增核心功能）

在原有 `vibe-coding-learning` Skill 基础上，新增两个能力：

#### F3.1 对话分析 → 学习洞察

| 分析维度 | 输出 |
|----------|------|
| 用户问了哪些类型的问题 | 分类统计（代码生成 / 调试 / 概念解释 / 架构设计） |
| 用户在哪些问题上反复追问 | 识别"未完全理解"的知识点，建议重点复习 |
| AI 的回答质量评估 | 对比公开最佳实践，标注 AI 回答中可能不准确的部分 |
| 学习进度推导 | 从对话历史推导用户的技术栈掌握程度（替代手动记录） |

#### F3.2 提示词优化指导

| 功能 | 说明 |
|------|------|
| 提示词模式识别 | 分析用户的历史提示词，识别高效 / 低效模式 |
| 优化建议 | 针对具体对话，给出"更好的提示词写法" |
| 参考公开资料 | 调用公开的 Prompt Engineering 资料（如 Anthropic Prompt Library、OpenAI Prompt Guide）作为指导依据 |
| 对比展示 | 改前 vs 改后的提示词 + 预期效果差异 |

---

### F4：知识笔记化（借鉴 NotebookLM + Obsidian）

| 借鉴来源 | 应用到本项目的设计 |
|-----------|----------------------|
| **NotebookLM** | 对话 → 自动生成摘要卡片；支持"问答模式"复习 |
| **Obsidian** | 双链笔记结构：`对话片段` ↔ `知识点` ↔ `代码片段`；支持 Graph View 展示知识关联 |
| **ima 知识库** | 左侧文件夹树 + 右侧内容区布局；支持按标签 / 项目 / AI 工具多维筛选 |

**输出结构**（与原有 Skill 的三层架构对齐）：
```
learning-notes/
├── topics/          ← 按对话会话聚合（对应 Obsidian 的 Daily Notes）
├── domains/         ← 按技术领域索引（对应 Obsidian 的 MOC）
└── cards/          ← 可复用知识卡片（对应 Obsidian 的 Zettelkasten）
```

---

### F5：本地文件同步

| 场景 | 处理方式 |
|------|----------|
| 项目代码更新 | 检测到 `src/` 等目录变化 → 提示"代码已更新，要重新分析对话上下文吗？" |
| AI 对话新增 | 检测到 `.workbuddy/` 等目录有新对话 → 提示"发现新对话，要导入吗？" |
| 手动刷新 | 用户点击"同步"按钮，重新扫描本地项目目录 |

**技术实现提示**（供 Codex 参考）：
- 浏览器端：File System Access API（`showDirectoryPicker`）获取目录句柄，持久化权限
- 服务端：用户安装本地同步 Agent（Python/Node 脚本），监听文件变化推送到网页端

---

## 三、页面布局设计

### 3.1 整体布局（参考 ima 知识库 + Obsidian）

```
┌──────────────────────────────────────────────────────────┐
│  Logo + 项目名            [搜索栏]    [同步] [设置]   │  ← 顶部栏
├──────────┬───────────────────────────────────────────────┤
│          │                                               │
│  左侧     │  主内容区                                      │
│  侧边栏   │                                               │
│          │                                               │
│  📁 项目  │  【默认视图：按项目聚合】                      │
│  🤖 AI   │                                               │
│  🏷 标签  │  ┌─────────────────────────────────────┐    │
│          │  │  2026-06-20 与 WorkBuddy 的对话       │    │
│  当前项目  │  │  ▸ FastAPI 登录模块开发               │    │
│  > my-   │  │    ✅ 知识点：JWT、bcrypt              │    │
│    project │  │    💬 对话片段（可展开）                │    │
│          │  │    📝 AI 生成的学习笔记                 │    │
│  所有项目  │  └─────────────────────────────────────┘    │
│          │                                               │
│  设置     │                                               │
└──────────┴───────────────────────────────────────────────┘
```

### 3.2 左侧侧边栏

| 模块 | 内容 |
|------|------|
| 项目列表 | 已导入的项目文件夹，点击切换 |
| AI 工具筛选 | 复选框：WorkBuddy / Claude / OpenClaw / Trae / Codex（默认全选 = 按项目聚合） |
| 标签筛选 | 按技术领域标签筛选（后端 / 前端 / AI / 等，自动从对话中提取） |
| 设置 | 本地路径配置、同步频率、导出格式 |

### 3.3 主内容区 — 对话详情页

```
┌─────────────────────────────────────────┐
│  📅 2026-06-20  │  ⏱ 耗时 45min  │  🏷 后端      │
├─────────────────────────────────────────┤
│                                         │
│  💬 对话摘要（AI 自动生成）              │
│  本次会话中，你与 WorkBuddy 合作完成了   │
│  FastAPI 登录注册模块，主要涉及...        │
│                                         │
│  ─── 对话时间线 ───                     │
│                                         │
│  [14:30] 你：帮我写一个登录接口          │
│  [14:31] AI：好的，这是代码...          │
│          ⚡ 提示词评分：7/10             │
│          💡 优化建议：加上"包含单元测试"  │
│                                         │
│  [14:40] 你：为什么用 bcrypt 不用 md5？ │
│  [14:41] AI：因为...                    │
│          ✅ 已理解（标记为掌握）           │
│                                         │
│  ─── 学习产出 ───                     │
│  📝 学习笔记  │  🗃 知识卡片  │  📊 进度更新│
│                                         │
└─────────────────────────────────────────┘
```

### 3.4 主内容区 — 提示词优化页（F3.2）

```
┌─────────────────────────────────────────┐
│  💡 提示词优化分析                      │
├─────────────────────────────────────────┤
│                                         │
│  📊 你的提示词风格分析                   │
│  ┌──────────┬──────────┬──────────┐  │
│  │ 具体程度  │ 上下文完整 │ 迭代次数  │  │
│  │   ⭐⭐⭐   │  ⭐⭐     │  平均 2.3 │  │
│  └──────────┴──────────┴──────────┘  │
│                                         │
│  💡 针对本次对话的优化建议               │
│                                         │
│  原提示词：                             │
│  > "帮我写一个登录接口"                  │
│                                         │
│  优化后：                               │
│  > "用 FastAPI 写一个登录接口，需要：    │
│  > 1. JWT token 认证                   │
│  > 2. bcrypt 密码加密                  │
│  > 3. 包含单元测试                     │
│  > 4. 解释为什么选择 JWT 而非 Session" │
│                                         │
│  📚 参考：Anthropic Prompt Library      │
│  🔗 链接：https://...                  │
│                                         │
└─────────────────────────────────────────┘
```

---

## 四、技术架构建议

### 4.1 技术栈（供 Codex 决策）

| 层级 | 推荐方案 | 理由 |
|------|----------|------|
| 前端 | **Next.js（App Router）+ Tailwind CSS** | 适合做知识库类界面，SSR 对 SEO 友好（参赛展示需要） |
| UI 组件 | **shadcn/ui** | 与 Tailwind 深度集成，适合做侧边栏、卡片、对话框 |
| 状态管理 | **Zustand** 或 **Jotai** | 轻量，适合局部状态多的知识库界面 |
| 本地文件访问 | **File System Access API**（浏览器端）或 **Electron**（桌面端） | 参赛原型建议先用浏览器端，降低用户使用门槛 |
| 数据存储 | **IndexedDB**（浏览器本地）+ 可选 **SQLite**（Electron 版） | 对话数据存在本地，隐私优先 |
| Markdown 渲染 | **react-markdown** + **remark-gfm** | 学习笔记以 Markdown 存储，需要渲染 |
| 代码高亮 | **shiki** 或 **highlight.js** | 对话中的代码片段需要语法高亮 |
| 知识图谱 | **D3.js** 或 **Cytoscape.js** | Obsidian 风格的双链图谱可视化（可后续迭代） |

### 4.2 数据结构设计

```typescript
// 项目
interface Project {
  id: string
  name: string
  localPath: string          // 本地路径（File System Access API 句柄）
  importedAt: Date
  lastSyncedAt: Date
  aiTools: AIToolType[]   // 检测到的 AI 工具列表
}

// AI 工具类型
type AIToolType = 'workbuddy' | 'claude' | 'openclaw' | 'trae' | 'codex'

// 对话会话
interface Conversation {
  id: string
  projectId: string
  aiTool: AIToolType
  startedAt: Date
  endedAt: Date
  messageCount: number
  messages: Message[]
}

// 对话消息
interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  codeSnippets: CodeSnippet[]
  timestamp: Date
}

// 代码片段
interface CodeSnippet {
  language: string
  code: string
  filePath?: string       // 关联的项目文件路径
  explanation?: string   // AI 的解释
}

// 学习笔记（与 Skill 输出对齐）
interface LearningNote {
  id: string
  conversationId: string
  date: string           // YYYY-MM-DD
  domain: string         // backend / frontend / etc.
  knowledgePoints: string[]
  noteContent: string    // Markdown
  cards: KnowledgeCard[]
}

// 知识卡片
interface KnowledgeCard {
  id: string
  category: string
  title: string
  content: string        // Markdown
  mastery: 'mastered' | 'understood' | 'exposed'
}

// 提示词分析
interface PromptAnalysis {
  conversationId: string
  score: number          // 1-10
  strengths: string[]
  weaknesses: string[]
  suggestions: {
    original: string
    improved: string
    reason: string
  }[]
  references: {
    title: string
    url: string
  }[]                  // 公开 Prompt Engineering 资料
}
```

---

## 五、与原有 Skill 的集成方案

### 5.1 Skill 新增功能（F3 对应）

在 `skills/vibe-coding-learning/SKILL.md` 中新增 **Mode 5**：

```markdown
### Mode 5: 对话分析与提示词优化（网页端触发，也可在 AI 对话中触发）

当用户说"分析一下我的对话记录"、"我的提示词写得怎么样"、"怎么问才能得到更好的回答"时触发。

执行步骤：

Step 1 — 读取对话历史
- 从 learning-notes/ 或网页端导入的对话数据中读取最近 N 次对话
- 提取用户的提示词模式和 AI 的回答质量

Step 2 — 分析提示词模式
- 分类统计：具体程度、上下文完整性、迭代次数、任务分解能力
- 识别低效模式：过于模糊、缺少约束条件、一次性抛多个问题

Step 3 — 生成优化建议
- 针对具体对话给出"改前 vs 改后"对比
- 引用公开 Prompt Engineering 资料（Anthropic / OpenAI 官方指南）
- 给出 1-3 条可操作的改进建议

Step 4 — 输出学习洞察
- 识别用户反复追问的知识点（= 未掌握）
- 推导技术栈掌握程度矩阵
- 建议下一步学习重点
```

### 5.2 网页端如何调用 Skill

| 场景 | 方式 |
|------|------|
| 用户在网页端点击"生成学习笔记" | 网页端调用本地 AI 工具（通过 CLI 或 API），传入 Skill 指令 |
| 用户在与 AI 对话时 | 直接说"帮我总结"，AI 调用 Skill 生成笔记，网页端可导入该笔记 |
| 提示词优化 | 网页端内置轻量分析逻辑（无需调用 Skill），Skill 的 Mode 5 作为增强版本 |

---

## 六、实施优先级（供 Codex 排期）

### Phase 1：基础原型（参赛截止前必须完成）

- [ ] 项目文件夹导入（手动选择路径）
- [ ] 识别 AI 工具目录
- [ ] 对话记录解析与展示（时间线视图）
- [ ] 基础布局：左侧边栏 + 右侧内容区
- [ ] Skill Mode 5 基础版（对话分析 + 提示词优化建议）

### Phase 2：增强功能（参赛后可迭代）

- [ ] 本地文件同步（File System Access API 持久化权限）
- [ ] 知识笔记化（对话 → Markdown 笔记，与 Skill 输出格式对齐）
- [ ] 提示词优化页（独立页面，带评分和建议）
- [ ] 按 AI 工具视图切换

### Phase 3：高级功能（后续版本）

- [ ] 知识图谱可视化（Obsidian 风格双链图谱）
- [ ] NotebookLM 式问答复习模式
- [ ] 多项目横向对比（跨项目的知识掌握度分析）
- [ ] 服务端版本（Team 协作，共享学习笔记）

---

## 七、参赛文章切入点建议

这篇文章/视频可以围绕以下角度展开（符合钳王争霸赛的"效率玩法与工作流实践"主题）：

**标题参考**：
> 《我用 WorkBuddy + 自建 Web Hub，把 5 个 AI 工具的编程对话变成了一座知识库》

**内容结构**：
1. 痛点：用 AI 编程很爽，但学过的东西转头就忘，对话记录散落各处
2. 方案：vibe-coding-learning Skill + Web Hub 组合拳
3. 实操：演示导入项目 → 自动聚合对话 → 生成学习笔记 → 提示词优化
4. 效果：学习进度可视化，面试前一键生成复习材料
5. 开源：GitHub 地址 + Skill 安装方式

**AI 率控制**：核心故事和个人体验用本人语言写，技术细节可借助 AI 整理（确保 AI 率 < 30%）。

---

## 八、给 Codex 的补充说明

1. **原型优先用静态 / 前端为主**：参赛展示需要能跑的 demo，建议先做前端原型（用 Next.js + Tailwind），数据先用 mock 数据，后续再接本地文件读取。

2. **移动端不需要**（参赛评审在桌面端查看），但布局要有响应式基础。

3. **UI 风格参考**：
   - ima 知识库：左侧深灰色侧边栏 + 右侧白色内容区
   - Obsidian：双链笔记的悬浮预览效果可以做简化版
   - NotebookLM：对话卡片的摘要折叠效果

4. **与 Skill 的分工**：
   - Skill（Markdown 指令）：运行在 AI 工具内部，负责"从代码/对话中提取知识"
   - Web Hub（网页应用）：负责"聚合展示 + 提示词分析 + 知识笔记化管理"
   - 两者通过 `learning-notes/` 目录作为数据交换层

---

*文档版本：v1.0 | 2026-06-21 | 作者：lyqqqq66666*
