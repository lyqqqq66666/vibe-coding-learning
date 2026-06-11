# vibe-coding-learning

> 把 Vibe Coding 变成真正的学习 — 让 AI 生成的代码不再只是"能跑"，而是"能懂"。

## 为什么需要它

AI 让写代码前所未有的快，但"理解代码"却越来越难：

- **"离开 AI 就不会写代码"** 已成为 2026 年开发者的集体焦虑，Meta 研究机构原计划的有/无 AI 对照实验因开发者集体拒绝在无 AI 环境下工作而被迫取消
- **AI 正在关上年轻人的入门通道** — 22-25 岁高暴露度职业就业率明显下滑，不是因为 AI 替代了老员工，而是替代了初级岗位
- **vibe coding 的产物无法在面试中讲清楚** — 能用 AI 生成登录注册模块，但说不清 JWT 原理、为什么用 bcrypt 而不是 md5

这个 Skill 做的就是：**每次 AI Coding 完成后，自动把代码变回知识**。

| 没有它 | 有了它 |
|--------|--------|
| AI 写完代码就结束，没有知识沉淀 | 自动生成学习笔记，形成"做中学"闭环 |
| 代码能跑但不知道学了什么 | 自动归纳知识点（JWT、Flexbox、状态管理等） |
| 看不懂 AI 生成的代码也不敢改 | 逐段讲解 + "为什么这样设计"追问 |
| 学了什么全凭记忆 | 学习日历 + 进度追踪 + 知识点卡片库 |
| 面试时讲不清项目 | Mode 4 按需生成面试话术和模拟提问 |

## 适用工具

本 Skill 是纯 Markdown 指令文件，任何能读取 SKILL.md 的 AI 编程工具均可使用：

| 工具 | 安装路径 | 触发方式 |
|------|---------|---------|
| **WorkBuddy** | `~/.workbuddy/skills/vibe-coding-learning/` | 编码完成后说"帮我总结" |
| **Trae** | `~/.trae/skills/vibe-coding-learning/` | 同上 |
| **Cursor** | `.cursor/rules/` | 引用 SKILL.md 指令 |
| **Claude Code** | `.claude/skills/` | `/vibe-coding-learning` |
| **OpenClaw** | skills 目录安装 | 对话触发 |
| **其他 AI Agent** | 任意可读 Markdown 指令的工具 | 引用 SKILL.md 即可 |

## 快速安装

**从 SkillHub（推荐）**
> 在 WorkBuddy 对话中输入：`安装 vibe-coding-learning skill`

**手动安装**
```bash
git clone https://github.com/lyqqqq66666/vibe-coding-learning.git
cp -r vibe-coding-learning/skills/vibe-coding-learning ~/.workbuddy/skills/
```

## 四种模式

| 模式 | 触发方式 | 做什么 |
|------|---------|--------|
| Mode 1: 生成笔记 | 完成编码后说"帮我总结" | 提取知识点 → 代码讲解 → 易错点 → 推荐资源 |
| Mode 2: 互动复习 | "帮我复习" | 先回忆 → 再揭晓答案 → 标记薄弱点 |
| Mode 3: 学习进度 | "学习进度" | 总览仪表盘 + 各领域进度条 |
| Mode 4: 面试准备 | "准备面试" / "模拟面试" | 基于已学内容生成话术和模拟提问 |

## 项目结构

```
skills/vibe-coding-learning/      # Skill 核心
├── SKILL.md                       # 主入口 + 四种模式工作流
├── references/                    # AI 参考手册
│   ├── knowledge-taxonomy.md       # 8 领域技术分类（基于 roadmap.sh）
│   ├── output-templates.md         # 产出物格式规范
│   ├── memory-management.md        # 三层归档策略
│   ├── tutorial-recommendation.md  # 教程搜索词库
│   ├── interview-prep.md           # Mode 4 面试策略
│   └── examples/                   # 三份完整示例笔记
└── templates/                      # 输出模板

examples/                          # 配套示例项目
├── backend-login/                 # FastAPI + JWT 登录注册
└── frontend-login/                # HTML/CSS/JS 登录注册

demo-output/                       # Skill 输出效果演示
├── topics/    domains/    cards/
├── calendar/  progress.md
```

## 许可证

MIT
