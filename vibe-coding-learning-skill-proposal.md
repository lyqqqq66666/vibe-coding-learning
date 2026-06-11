# Vibe Coding Learning Skill 方案设计

> **PROPOSAL v1.0** | 2026-06-11 | 基于 Trae Skill 规范

---

## 目录

1. [背景与痛点分析](#一背景与痛点分析)
2. [Skill 定位与核心价值](#二skill-定位与核心价值)
3. [Skill 架构设计](#三skill-架构设计)
4. [核心工作流详解](#四核心工作流详解)
5. [技术覆盖范围（知识图谱）](#五技术覆盖范围知识图谱)
6. [输出格式与模板设计](#六输出格式与模板设计)
7. [记忆与知识管理体系](#七记忆与知识管理体系)
8. [扩展功能：求职导向](#八扩展功能求职导向)
9. [需要用户手动准备的工具与 Skill 清单](#九需要用户手动准备的工具与-skill-清单)
10. [实施路线图](#十实施路线图)
11. [下一步行动](#十一下一步行动)

---

## 一、背景与痛点分析

### 1.1 AI 时代的编程学习困境

2025 年 Andrej Karpathy 提出 **Vibe Coding** 概念，核心理念是"用自然语言描述需求，让 AI 生成代码"。这一范式迅速席卷开发社区，但也带来了一个严峻的教育问题：

> **核心矛盾**：AI 让"写代码"变得前所未有的容易，但**"理解代码"却变得越来越难**。学生可以用 AI 在 40 秒内生成一个登录注册模块，但可能完全不理解 JWT 认证、Session 管理、密码哈希等背后的原理。

### 1.2 计算机专业学生的具体痛点

| 痛点 | 描述 |
|------|------|
| **技能退化焦虑** | "离开 AI 就不会写代码"已成为 2026 年开发者的集体现象。METR 研究机构原计划开展"有 AI vs 无 AI"对照实验，因开发者集体拒绝在无 AI 环境下工作而被迫取消 [1]。 |
| **就业焦虑** | Anthropic 研究揭示：AI 并未大规模淘汰老员工，而是让 22-25 岁年轻人的高暴露度职业就业率明显下滑——AI 正在关上年轻人的"入门通道" [2]。 |
| **认知疲惫** | 2025 年全球 AI 模型发布量突破三位数，技术迭代速度远超学习能力。89.2% 受访者感觉自己过于依赖 AI，54.9% 担心过度依赖会忽略自身成长 [2]。 |
| **基础薄弱** | 一位计算机教授指出：2023 年学生用 ChatGPT 写作业尚可查出，2026 年学生用 Cursor 写作业已无法分辨，学生自己也分不清哪些代码是自己写的 [1]。 |

### 1.3 市场空白

经过调研，skills.sh 上已有 **24 万+** 技能包，但**几乎没有专门的"学习总结""知识提取""学习进度跟踪"类 Skill**。这是一个明确的市场空白，也是本 Skill 的核心机会。

---

## 二、Skill 定位与核心价值

### 2.1 一句话定位

> **vibe-coding-learning**：当用户完成一次 AI Coding 任务后，自动将代码变更转化为结构化的学习笔记、知识点归纳和代码讲解，帮助计算机专业学生从 Vibe Coding 中真正学到技术。

### 2.2 核心价值主张

| 维度 | 没有这个 Skill | 有了这个 Skill |
|------|---------------|---------------|
| **学习闭环** | AI 写完代码就结束，没有知识沉淀 | 每次 AI Coding 自动生成学习笔记，形成"做中学"闭环 |
| **知识点提取** | 代码能跑但不知道学了什么 | 自动归纳涉及的知识点（JWT、RESTful、状态管理等） |
| **代码理解** | AI 生成的代码看不懂也不敢改 | 逐段代码讲解 + "为什么这样设计" + 设计模式识别 |
| **学习进度** | 学了什么全凭记忆，无法回顾 | 学习日历 + 进度追踪 + 知识图谱式分类 |
| **易错点** | 踩过的坑下次还踩 | 自动整理常见错误和注意事项 |
| **扩展学习** | 不知道下一步该学什么 | 推荐相关教程（B 站、文档等）和进阶方向 |

### 2.3 适用场景（不限于特定 AI 工具）

本 Skill 设计为**工具无关**，无论用户使用以下哪种 AI Coding 工具，都可以在任务完成后调用本 Skill 来生成学习笔记：

| 工具 | 加载方式 | 备注 |
|------|---------|------|
| **Trae / WorkBuddy** | 原生 Skill 支持，直接触发 | 推荐 |
| **Claude Code** | 通过 `.claude/skills/` 目录加载 | |
| **Cursor** | 通过 `.cursor/rules/` 加载 | |
| **OpenAI Codex** | 通过指令引用 SKILL.md | |
| **GitHub Copilot** | 通过 Copilot Instructions 引用 | |
| **其他 AI Agent** | 任何支持读取 Markdown 指令的 AI 工具 | |

---

## 三、Skill 架构设计

### 3.1 整体架构

根据 Trae 官方 Skill 编写最佳实践，本 Skill 遵循以下设计原则：

- **职责单一**：只做一件事——将 AI Coding 的代码变更转化为学习笔记
- **边界明确**：正向条件（什么时候用）和负向条件（什么时候不用）都清晰定义
- **渐进式披露**：SKILL.md 作为入口，详细模板和参考文件拆分到 references/ 目录
- **输入输出结构化**：明确定义 Input 和 Output 格式

### 3.2 Skill 目录结构

```
skills/vibe-coding-learning/
├── SKILL.md                          # 主入口（控制在 500 行以内）
├── references/
│   ├── knowledge-taxonomy.md          # 编程技术知识分类体系
│   ├── output-templates.md            # 输出模板（MD + HTML）
│   ├── memory-management.md           # 记忆与知识管理策略
│   ├── tutorial-recommendation.md    # 教程推荐策略与资源库
│   ├── interview-prep.md             # 面试准备扩展模块
│   └── examples/
│       ├── example-backend-auth.md    # 示例：后端认证学习笔记
│       ├── example-frontend-react.md # 示例：前端 React 学习笔记
│       └── example-agent-langgraph.md# 示例：AI Agent 学习笔记
└── templates/
    ├── daily-learning-note.md        # 每日学习笔记模板
    ├── knowledge-point.md             # 知识点卡片模板
    └── learning-calendar.md            # 学习日历模板
```

### 3.3 SKILL.md 核心结构（草案）

```yaml
---
name: vibe-coding-learning
description: >
  Generate structured learning notes from AI coding sessions.
  Use when the user has just completed a coding task with AI assistance
  and wants to summarize what was learned, understand the generated code,
  extract knowledge points, and track learning progress.
  Covers all programming domains: full-stack, testing, AI/ML, DevOps,
  cloud, mobile, data engineering, and cybersecurity.
---
```

**Use this skill when:**
- User just completed a coding task with AI and wants a learning summary
- User asks to "summarize today's learning", "explain this code", "extract knowledge points"
- User wants to build a learning note from a vibe coding session
- User references "learning calendar", "learning progress", or "knowledge map"

**Do NOT use this skill when:**
- User is still in the middle of coding and hasn't asked for a summary
- User only wants code review or bug fixing without learning context
- User asks about non-programming topics

**Input:**
- `coding_session_context`: What the user built with AI today
- `changed_files`: List of files created or modified
- `user_background`: CS student level (optional)
- `preferred_format`: md | html (default: md)

**Output:**
- `learning_note`: Structured markdown/html document
- `knowledge_points`: Extracted knowledge point cards
- `learning_calendar_update`: Calendar entry for today
- `tutorial_recommendations`: Curated learning resources

---

## 四、核心工作流详解

当用户完成一次 AI Coding 任务后，调用本 Skill 的完整工作流如下：

### Step 1：收集上下文
读取本次 AI Coding 会话中创建/修改的文件列表，分析代码变更内容。如果用户提供了项目目录，扫描目录结构理解项目全貌。

### Step 2：识别技术领域
根据代码内容，自动识别涉及的技术领域（如"后端认证"、"前端状态管理"、"AI Agent 开发"等），参照 `references/knowledge-taxonomy.md` 中的分类体系进行归类。

### Step 3：提取知识点
从代码变更中归纳知识点。例如用户用 AI 做了登录注册逻辑，应提取：JWT 认证原理、密码哈希（bcrypt）、RESTful API 设计、数据库模型设计、中间件机制等知识点。

### Step 4：逐段代码讲解
对关键代码文件进行逐段解读：先读哪里、核心逻辑在做什么、为什么这样设计、用了什么设计模式、如果不用 AI 自己该怎么写。

### Step 5：整理易错点
基于代码分析 + 通用知识，整理该技术领域的常见错误和注意事项。例如：JWT 过期处理、SQL 注入防护、XSS 防御等。

### Step 6：推荐教程
结合提取的知识点，推荐相关的学习资源（B 站教程、官方文档、技术博客等）。可通过 Web Search MCP 或内置资源库来获取推荐。

### Step 7：更新学习日历
将本次学习内容记录到学习日历中，标记日期、技术领域、知识点数量。判断是否与已有学习主题关联，决定是追加到已有文件夹还是创建新的学习主题。

### Step 8：生成输出文件
按用户选择的格式（MD 或 HTML）生成学习笔记文件，保存到指定目录。同时更新学习进度索引文件。

### 4.1 记忆管理策略（"像人一样学习"）

你提到的"像人的记忆一样"的组织方式，具体实现如下：

> **记忆分类决策树**：每次生成学习笔记时，Skill 会执行以下判断：
> 1. **已有相关主题？** → 检查学习目录中是否已有相同技术领域的文件夹（如 `backend-auth/`、`react-frontend/`）
> 2. **有 → 追加** → 在已有文件夹中创建新的日期笔记，更新该主题的索引文件
> 3. **没有 → 新建** → 创建新的主题文件夹，建立主题索引，记录到学习日历
> 4. **跨主题？** → 如果本次学习涉及多个领域（如"后端 + 前端 + 部署"），在各自主题文件夹中创建交叉引用

**学习笔记的目录结构示例：**

```
learning-notes/
├── README.md                    # 学习总览与进度仪表盘
├── calendar/
│   ├── 2026-06.md              # 2026年6月学习日历
│   └── 2026-07.md
├── progress.md                  # 学习进度总览
├── backend-auth/                # 主题：后端认证
│   ├── _index.md               # 主题索引（知识点清单、学习路径）
│   ├── 2026-06-11-login-register.md  # Day 1 笔记
│   └── 2026-06-15-jwt-refresh.md     # Day 2 笔记
├── react-frontend/             # 主题：React 前端
│   ├── _index.md
│   └── 2026-06-20-component-patterns.md
├── ai-agent/                   # 主题：AI Agent 开发
│   ├── _index.md
│   └── 2026-06-25-langgraph-basic.md
└── knowledge-points/            # 知识点卡片库（可跨主题引用）
    ├── jwt-authentication.md
    ├── restful-api-design.md
    ├── react-hooks.md
    └── langgraph-state.md
```

---

## 五、技术覆盖范围（知识图谱）

本 Skill 的知识分类体系覆盖计算机专业学生可能接触的**所有主流编程技术方向**。

### 5.1 八大技术领域

| 领域 | 子领域 | 代表技术 |
|------|--------|---------|
| **全栈 Web 开发** | 前端基础 | HTML5, CSS3, JavaScript (ES2024+), TypeScript |
| | 前端框架 | React, Vue 3, Angular, Svelte, Next.js, Nuxt.js |
| | 后端框架 | FastAPI, Django, Express, Spring Boot, Gin, NestJS |
| | 数据库 | PostgreSQL, MySQL, MongoDB, Redis, Prisma, SQLAlchemy |
| **测试** | 单元/集成测试 | Jest, Vitest, Pytest, JUnit, Go testing |
| | E2E 测试 | Playwright, Cypress, Selenium |
| | 性能测试 | k6, JMeter, Locust |
| **AI / ML 开发** | 机器学习 | Scikit-learn, Pandas, NumPy |
| | 深度学习 | PyTorch, TensorFlow, JAX |
| | LLM 应用 | LangChain, LlamaIndex, RAG, Prompt Engineering |
| | AI Agent | LangGraph, AutoGen, CrewAI, Claude Code SDK, MCP |
| **DevOps** | 容器化 | Docker, Kubernetes, Docker Compose |
| | CI/CD | GitHub Actions, GitLab CI, Jenkins, ArgoCD |
| | IaC | Terraform, Ansible, Pulumi |
| **云计算** | 公有云 | AWS, GCP, Azure, 阿里云, 腾讯云 |
| | Serverless | AWS Lambda, Cloudflare Workers, Vercel |
| **移动开发** | 跨平台 | React Native, Flutter, Expo |
| | 小程序 | 微信小程序, Taro, uni-app |
| **数据工程** | 数据管道 | Apache Kafka, Spark, Airflow, dbt |
| | 数据仓库 | Snowflake, BigQuery, ClickHouse |
| **网络安全** | Web 安全 | OWASP Top 10, XSS/CSRF/SQL 注入防护 |
| | 认证授权 | OAuth 2.0, JWT, SAML, RBAC/ABAC |

### 5.2 知识点提取策略

对于每个技术领域，Skill 内置了**知识点模板库**。例如当识别到"后端认证"领域时，自动关联以下知识点维度：

- **核心概念**：认证 vs 授权、Session vs Token、无状态认证
- **技术实现**：密码哈希算法、JWT 签发与验证、Refresh Token 机制
- **安全要点**：SQL 注入、XSS、CSRF 防护、HTTPS、CORS 配置
- **设计模式**：中间件模式、策略模式、仓储模式、DTO 模式

---

## 六、输出格式与模板设计

### 6.1 每日学习笔记模板

```markdown
# [日期] [技术主题] — 学习笔记

## 基本信息
- **日期**：2026-06-11
- **技术领域**：后端开发 / 认证与安全
- **AI 工具**：Trae / Claude Code / Cursor
- **任务描述**：用 AI 实现了用户登录注册的后端逻辑

## 知识点归纳
### 1. JWT 认证机制
- **是什么**：JSON Web Token，一种无状态的认证方式
- **核心流程**：用户登录 → 服务端签发 Token → 客户端存储 → 每次请求携带 → 服务端验证
- **关键代码**：`auth.py` 第 23-45 行

### 2. 密码哈希（bcrypt）
- **为什么不能明文存储密码**
- **bcrypt 的工作原理**：加盐 + 多轮哈希
- **关键代码**：`auth.py` 第 12-20 行

### 3. RESTful API 设计
- **POST /auth/register** vs **POST /auth/login**
- **请求/响应格式规范**

## 代码讲解
### 先读哪里
建议阅读顺序：`models.py` → `auth.py` → `routes.py` → `middleware.py`

### 逐段解读
#### models.py — 用户模型定义
[逐段代码解读，解释每个字段的含义和设计考量]

#### auth.py — 认证核心逻辑
[逐段代码解读，解释 JWT 签发、密码验证流程]

### 为什么这样设计
- 为什么用 JWT 而不是 Session？
- 为什么密码要用 bcrypt 而不是 md5？
- 为什么要把认证逻辑拆成单独的 service 层？

## 易错点整理
| 易错点 | 正确做法 | 常见错误 |
|--------|---------|---------|
| 密码存储 | bcrypt 哈希 | 明文存储或用 md5 |
| Token 传输 | Authorization Header | 放在 URL 参数中 |
| 错误信息 | "用户名或密码错误" | "密码错误"（泄露用户名存在） |

## 推荐学习资源
- [B 站] JWT 认证原理精讲（搜索关键词：JWT 原理 认证）
- [文档] FastAPI 官方文档 — Security 章节
- [博客] 理解 OAuth 2.0 和 JWT 的区别

## 面试怎么讲
"我在项目中实现了基于 JWT 的用户认证系统。用户注册时密码用 bcrypt 哈希存储，
登录后签发 Access Token 和 Refresh Token。Access Token 有效期 15 分钟，
Refresh Token 7 天，通过中间件自动验证..."

## 下一步学习建议
- [ ] 了解 Refresh Token 轮转机制
- [ ] 学习 OAuth 2.0 第三方登录
- [ ] 尝试实现 RBAC 角色权限管理
```

### 6.2 HTML 格式支持

除了 Markdown 格式，Skill 还支持生成精美的 HTML 学习笔记页面，具备以下特性：

- 响应式布局，支持手机/平板/电脑阅读
- 代码高亮显示
- 知识点卡片式展示
- 内置目录导航
- 学习进度可视化

### 6.3 知识点卡片模板

```markdown
---
type: knowledge-point
domain: backend
topic: authentication
related_files: [auth.py, middleware.py, models.py]
difficulty: intermediate
tags: [jwt, bcrypt, rest-api, security]
---

# JWT 认证机制

## 一句话定义
JSON Web Token 是一种基于 JSON 的开放标准（RFC 7519），用于在各方之间安全地传输信息。

## 核心组成
- Header：算法和类型
- Payload：有效载荷（用户信息）
- Signature：签名（防篡改）

## 工作流程
1. 用户提交用户名和密码
2. 服务端验证通过后，用私钥签发 JWT
3. 客户端存储 JWT（通常在 localStorage 或 Cookie）
4. 后续请求在 Authorization Header 中携带 JWT
5. 服务端验证签名和有效期

## 常见误区
- ❌ 在 JWT 中存储敏感信息（Payload 只是 Base64 编码，不是加密）
- ❌ JWT 过期时间设置过长
- ❌ 不验证签名

## 相关知识点
- OAuth 2.0
- Session vs Token
- Refresh Token 机制
```

---

## 七、记忆与知识管理体系

### 7.1 三层记忆架构

```
┌─────────────────┐     每日沉淀      ┌─────────────────┐     定期整理      ┌─────────────────┐
│  Session Memory  │ ──────────────→  │   Topic Memory   │ ──────────────→  │ Knowledge Graph  │
│    会话记忆       │                  │    主题记忆        │                  │    知识图谱       │
└─────────────────┘                  └─────────────────┘                  └─────────────────┘
        │                                     │                                     │
   当日代码变更                           backend-auth/                        知识点卡片库
   即时笔记                              react-frontend/                      跨主题关联
                                         ai-agent/                           学习路径图
```

### 7.2 学习进度追踪

`progress.md` 文件记录整体学习进度，格式如下：

```markdown
# 学习进度总览

## 统计
- 总学习天数：15 天
- 已覆盖领域：3 / 8
- 已掌握知识点：42 个
- 已完成项目：2 个

## 领域进度
| 领域 | 进度 | 笔记数 | 知识点数 | 最近更新 |
|------|------|--------|---------|---------|
| 全栈 Web | ██████░░░░ 60% | 8 | 18 | 2026-06-11 |
| AI/ML | ███░░░░░░░ 30% | 3 | 9 | 2026-06-08 |
| 测试 | ░░░░░░░░░░ 0% | 0 | 0 | - |

## 学习日历
### 2026-06
| 日期 | 主题 | 关键词 | 笔记链接 |
|------|------|--------|---------|
| 06-11 | 后端认证 | JWT, bcrypt, REST | [笔记](backend-auth/2026-06-11-login-register.md) |
| 06-08 | LangGraph 基础 | StateGraph, Node, Edge | [笔记](ai-agent/2026-06-08-langgraph-basic.md) |
| 06-05 | React Hooks | useState, useEffect | [笔记](react-frontend/2026-06-05-hooks.md) |
```

---

## 八、扩展功能：求职导向

### 8.1 与校招 Skill 的联动

你提到的"结合 WorkBuddy 或 IMA 使用腾讯校招的 Skill"是一个很好的扩展方向。具体联动方式如下：

> **求职学习闭环：**
> 1. **了解目标**：用户先通过校招 Skill（如腾讯 IMA 的校招助手）了解目标岗位的技术要求
> 2. **制定计划**：根据岗位 JD，结合本 Skill 的知识分类体系，生成有针对性的学习计划
> 3. **实践学习**：通过 Vibe Coding 完成相关项目，本 Skill 自动生成学习笔记
> 4. **面试准备**：每个知识点卡片中包含"面试怎么讲"模块，可直接用于面试准备
> 5. **查漏补缺**：对比岗位要求和已掌握知识点，自动识别差距并推荐学习内容

### 8.2 面试准备模块

每个学习笔记中的"面试怎么讲"模块，会根据知识点生成 30-90 秒的表达模板。例如：

**30 秒版：**
> "我在项目中用 FastAPI + JWT 实现了用户认证系统。注册时密码用 bcrypt 哈希，登录后签发 Access Token 和 Refresh Token，通过中间件统一拦截验证。整个认证逻辑拆分为 auth service、middleware、routes 三层，方便后续扩展。"

**90 秒版：**
> "我在一个全栈项目中独立负责了用户认证模块的设计和实现。技术选型上，我对比了 Session 和 JWT 两种方案，考虑到项目后续需要支持多端接入和水平扩展，最终选择了无状态的 JWT 方案。具体实现上，密码存储使用 bcrypt 算法加盐哈希，Token 签发使用 RS256 非对称加密。Access Token 有效期设为 15 分钟，Refresh Token 7 天，通过 Refresh Token 轮转机制来提升安全性。架构上，我把认证逻辑拆成了独立的 auth service 层，通过 FastAPI 的依赖注入机制实现中间件级别的 Token 验证，这样业务代码不需要关心认证细节。后续我还计划接入 OAuth 2.0 支持第三方登录。"

### 8.3 目标岗位技术要求映射

| 目标岗位 | 核心技术要求 | 对应 Skill 学习主题 |
|---------|------------|-------------------|
| 后端开发（实习） | 语言基础、数据库、API 设计、Linux | 全栈 Web + DevOps |
| 前端开发（实习） | HTML/CSS/JS、框架、工程化 | 全栈 Web（前端方向） |
| AI 算法（实习） | Python、ML/DL、模型训练 | AI/ML 开发 |
| AI 应用（实习） | LLM 应用、RAG、Agent | AI/ML（Agent 方向） |
| 测试开发（实习） | 自动化测试、CI/CD、质量保障 | 测试 + DevOps |
| 运维/DevOps（实习） | Docker、K8s、CI/CD、监控 | DevOps + 云计算 |

---

## 九、需要用户手动准备的工具与 Skill 清单

为了让本 Skill 发挥最大效果，以下是你需要手动准备或了解的工具和资源：

### 9.1 必须准备的（核心依赖）

| 工具/资源 | 用途 | 获取方式 | 优先级 |
|----------|------|---------|--------|
| **Trae IDE** | Skill 的原生运行环境，SOLO 模式支持 | [trae.ai](https://www.trae.ai) 下载安装 | **必须** |
| **Web Search 能力** | 搜索教程推荐、技术文档 | Trae 内置 WebSearch 工具，或安装 Tavily/Brave Search MCP | **必须** |
| **Memory MCP Server** | 跨会话记忆持久化，知识图谱构建 | Trae MCP 市场安装，或从 GitHub 获取开源方案 | **必须** |

### 9.2 推荐安装的（增强体验）

| 工具/资源 | 用途 | 获取方式 | 优先级 |
|----------|------|---------|--------|
| **Sequential Thinking MCP** | 结构化思维流程，帮助拆解复杂知识点 | Trae MCP 市场搜索安装 | 推荐 |
| **Context7 MCP** | 实时获取官方文档最新内容和代码示例 | Trae MCP 市场搜索安装 | 推荐 |
| **Playwright MCP** | 浏览器自动化，抓取教程网页内容 | Trae MCP 市场搜索安装 | 推荐 |
| **GitHub MCP** | 代码搜索、开源项目学习 | Trae MCP 市场搜索安装 | 推荐 |
| **html-report Skill** | 生成精美的 HTML 格式学习笔记 | Trae 内置 Skill | 推荐 |

### 9.3 可选的（扩展功能）

| 工具/资源 | 用途 | 获取方式 | 优先级 |
|----------|------|---------|--------|
| **腾讯 IMA 校招 Skill** | 了解目标岗位技术要求，制定学习计划 | 腾讯 IMA 平台搜索"校招"相关 Skill | 可选 |
| **WorkBuddy** | 桌面 AI 助手，支持技能平台和腾讯生态 | [workbuddy.tencent.com](https://workbuddy.tencent.com) | 可选 |
| **Understand-Anything** | 将代码库转为可交互知识图谱 | GitHub 开源项目（3万+ Star） | 可选 |
| **Claude-Mem** | Claude Code 跨会话持久化记忆 | GitHub 开源项目（3万+ Star） | 可选 |
| **skill-creator Skill** | 帮助创建和迭代 Skill | Trae 内置 Skill | 可选 |
| **mcp-omnisearch** | 一站式搜索，整合多个搜索引擎 | GitHub 开源 MCP Server | 可选 |

### 9.4 需要手动收集的资源

| 资源类型 | 说明 | 如何准备 |
|---------|------|---------|
| **B 站教程收藏** | 各技术领域的优质教程链接 | 手动收集或让 AI 通过 Web Search 搜索整理 |
| **目标岗位 JD** | 你心仪公司的校招/实习岗位描述 | 从招聘网站收集，保存为 Markdown |
| **个人学习目标** | 你希望掌握的技术栈和优先级 | 写一份简单的学习目标文档 |

---

## 十、实施路线图

按照 Trae 官方推荐的"评测驱动、失败优先"的 Skill 构建流程 [3]，建议分以下阶段推进：

### Phase 1：最小可用版本（MVP）

> **目标：1-2 天内完成** — 创建最简单的 Skill，能在一个具体场景下稳定工作。

1. **新建测试项目**：在一个空文件夹中，用 Trae SOLO 模式让 AI 做一个简单的登录注册后端（FastAPI + JWT）
2. **无 Skill 基线测试**：完成后直接让 AI "帮我总结今天的学习内容"，记录输出质量
3. **编写最小 SKILL.md**：只包含核心触发条件 + 8 步工作流 + 输出模板
4. **评测对比**：用同样的请求，对比有无 Skill 的输出质量差异

### Phase 2：完善知识体系

> **目标：3-5 天内完成** — 扩展知识分类体系，增加更多领域的支持。

1. 编写 `references/knowledge-taxonomy.md`（完整的八大领域知识分类）
2. 为 3-5 个常见场景编写示例笔记（后端认证、React 组件、API 设计等）
3. 完善记忆管理策略，实现"主题文件夹 + 知识点卡片"的组织方式
4. 增加 HTML 输出格式支持

### Phase 3：增强功能

> **目标：1-2 周内完成** — 增加教程推荐、面试准备、求职联动等高级功能。

1. 集成 Web Search，实现自动教程推荐
2. 完善面试准备模块，增加不同时长的表达模板
3. 设计求职联动方案，支持导入岗位 JD 自动生成学习计划
4. 增加学习进度可视化和统计功能

### Phase 4：测试与迭代

1. 在不同 AI 工具上测试（Trae、Claude Code、Cursor）
2. 邀请同学试用，收集反馈
3. 根据真实使用数据持续迭代优化

---

## 十一、下一步行动

> **建议立即开始的第一步**：新建一个空文件夹作为测试项目，用 Trae 的 SOLO 模式让 AI 帮你做一个简单的后端登录注册功能（比如 FastAPI + JWT + SQLite），完成后调用本 Skill 生成第一份学习笔记。这是验证整个流程的最小可行测试。

**具体操作步骤：**

1. 在 Trae 中新建一个项目文件夹（如 `test-login-project/`）
2. 用 SOLO 模式描述需求："帮我用 FastAPI 实现一个用户登录注册的后端，包括 JWT 认证和密码哈希"
3. AI 完成编码后，输入："调用 vibe-coding-learning skill，帮我总结今天的学习内容"
4. 查看生成的学习笔记质量，记录哪些地方需要改进
5. 根据测试结果，迭代优化 SKILL.md

> **重要提醒**：根据 Trae 官方最佳实践，**不要一开始就追求完美**。先写一个能通过一个具体场景的最小 Skill，然后通过"评测 → 发现问题 → 修改 Skill → 再评测"的循环逐步完善。Skill 的质量来自于真实使用中的迭代，而不是初始设计的完美。

等你确认方案后，我可以立即帮你：

1. 创建 `skills/vibe-coding-learning/SKILL.md` 的完整初版
2. 创建配套的 references/ 和 templates/ 文件
3. 搭建测试项目并生成第一份示例学习笔记

---

## Sources

1. ["离开AI我就不会写代码了": 2026年开发者集体成瘾与技能退化危机](https://m.toutiao.com/group/7647727410305188358/)
2. [为什么越来越多人开始焦虑AI? — AI焦虑深度分析](https://m.toutiao.com/group/7645966857559884323/)
3. [Trae 官方文档：如何写好一个 Skill — 从创建到迭代的最佳实践](https://docs.trae.ai/ide/best-practice-for-how-to-write-a-good-skill?_lang=zh)
4. [AI编程爆发后，为什么你写代码快了17倍却更焦虑了?](https://m.toutiao.com/group/7649580943891563044/)
5. [席卷AI编程圈的十大Skills! skills.sh最新榜单](https://m.toutiao.com/group/7634001161279783430/)
6. [AI时代的知识内化，写个SKILL就够了](https://m.toutiao.com/group/7608958273269596699/)
7. [TRAE IDE 10大热门MCP Server推荐](https://m.toutiao.com/group/7598611824879141430/)
8. [awesome-claude-code: Claude Code最强资源宝库 (40.4k+ stars)](https://m.toutiao.com/group/7631770835551846921/)
9. [Understand-Anything: 将代码库变成可交互知识图谱 (3万+ stars)](https://m.toutiao.com/group/7643974166848307752/)
10. [学生免费编程工具：2026最新热门AI编程工具必看](https://m.toutiao.com/group/7649267175450067491/)
