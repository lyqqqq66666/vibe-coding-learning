# vibe-coding-learning

> 把 Vibe Coding 变成真正的学习 — 让 AI 生成的代码不再只是"能跑"，而是"能懂"。

## 一句话

让 CS 学生在用 AI 写代码后，自动生成结构化学习笔记、知识点归纳和代码讲解，从"靠 AI 堆代码"变成"靠 AI 学技术"。

## 为什么需要它

AI 让写代码前所未有的快，但"理解代码"却越来越难。这个 Skill 解决的就是：**每次 AI Coding 完成后的知识沉淀**。

## 快速安装

这是一个 WorkBuddy / Trae 的 Agent Skill。

**方式一：从 SkillHub 安装**
> 在 WorkBuddy 对话中输入：`安装 vibe-coding-learning skill`

**方式二：手动安装**
将 `skills/vibe-coding-learning/` 复制到你的 WorkBuddy skills 目录：
```bash
cp -r skills/vibe-coding-learning ~/.workbuddy/skills/
```

## 功能

| 模式 | 触发方式 | 做什么 |
|------|---------|--------|
| Mode 1: 生成笔记 | 完成编码后说"帮我总结" | 提取知识点 → 代码讲解 → 易错点 → 推荐资源 |
| Mode 2: 互动复习 | "帮我复习" | 先让你回忆 → 再揭晓答案 → 标记薄弱点 |
| Mode 3: 学习进度 | "学习进度" | 总览仪表盘 + 各领域进度条 |
| Mode 4: 面试准备 | "准备面试" / "模拟面试" | 基于你学过的内容生成面试话术和模拟提问 |

## 目录

```
skills/vibe-coding-learning/      # Skill 核心
├── SKILL.md                       # 主入口 + 四种模式工作流
└── templates/                     # 输出模板

examples/                          # 配套示例项目
├── backend-login/                 # FastAPI + JWT 登录注册后端
└── frontend-login/                # HTML/CSS/JS 登录注册前端

demo-output/                       # Skill 输出效果演示
├── topics/                        # 按项目的学习笔记
├── domains/                       # 按技术领域的知识索引
├── cards/                         # 可复用知识点卡片
├── calendar/                      # 学习日历
└── progress.md                    # 学习进度总览
```

## 适用场景

- 用 AI 完成了编码，想总结学了什么
- Vibe Coding 过程中想理解 AI 生成的代码
- 想追踪自己各技术领域的学习进度
- 准备面试时想回顾做过的项目

## 许可证

MIT
