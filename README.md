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
| **Trae** | `~/.trae-cn/skills/vibe-coding-learning/` | 同上 |
| **Claude Code** | `~/.claude/skills/vibe-coding-learning/` | `/vibe-coding-learning` |
| **OpenClaw** | `~/.openclaw/skills/vibe-coding-learning/` | 对话触发 |
| **Codex** | `~/.codex/skills/vibe-coding-learning/` | 对话触发 |
| **Cursor** | 手动导入或引用 SKILL.md | 引用指令 |
| **其他 AI Agent** | 任意可读 Markdown 指令的工具 | 引用 SKILL.md 即可 |

## 安装

### 方式一：手动复制（适合最终用户）

```bash
git clone https://github.com/lyqqqq66666/vibe-coding-learning.git
cp -r vibe-coding-learning/skills/vibe-coding-learning ~/.workbuddy/skills/
```

各工具路径见上方兼容表，换一下目标目录即可。

### 方式二：使用同步脚本（推荐，适合所有用户）

项目自带 `sync-skills.sh`，一键同步到所有已安装的 AI 工具：

```bash
git clone https://github.com/lyqqqq66666/vibe-coding-learning.git
cd vibe-coding-learning

# 预览同步目标
bash sync-skills.sh --dry-run

# 执行同步（自动同步到所有 enabled 的工具）
bash sync-skills.sh

# 只同步到指定工具
bash sync-skills.sh --target=workbuddy
```

如果某个工具未安装，编辑 `sync-config.json` 将对应 `enabled` 改为 `false` 即可跳过。

### 方式三：自动同步（适合开发者）

如果你参与 Skill 开发，可以激活 Git Hooks，每次 `git push main` 或 `git merge dev` 后自动同步：

```bash
cd vibe-coding-learning
git config core.hooksPath .githooks
```

激活后，以下操作会自动触发同步：
- `git push origin main` → 推送到 main 后自动同步
- `git merge dev`（在 main 上）→ 合并后自动同步

> ⚠️ 注意：dev 分支推送不会触发同步，只有 main 分支会。

## 更新 Skill

当 GitHub 上的 Skill 有更新时，重新同步即可：

```bash
cd vibe-coding-learning
git pull origin main
bash sync-skills.sh
```

## 九种模式

| 模式 | 触发方式 | 做什么 |
|------|---------|--------|
| Mode 1: 生成笔记 | "总结今天学的"、"这段代码讲一下" | 提取知识点 → 代码讲解 → 易错点 → 推荐资源（支持 light/standard/deep 三档） |
| Mode 2: 互动复习 | "复习昨天的"、"帮我测一下 JWT" | 先回忆 → 再揭晓答案 → 标记薄弱点 |
| Mode 3: 学习进度 | "我学了多少了"、"学习进度怎么样" | 总览仪表盘 + 各领域 mastery ratio |
| Mode 4: 面试准备 | "准备面试" / "模拟面试" | 基于已学内容生成话术和模拟提问 |
| Mode 5: 提示词优化 | "我的提示词怎么样"、"怎么问才能得到更好回答" | 分析对话质量 → 提示词评分 → 改前改后对比 |
| Mode 6: 收件箱整理 | "有什么没整理的笔记吗" | 扫描未处理会话 → 批量整理 → 状态流转 |
| Mode 7: 知识关联 | "今天学的和之前有什么关联" | 自动关联新旧知识 → 交叉引用 → 知识成网 |
| Mode 8: 深度周总结 | "周总结"、"这周学了什么" | 领域覆盖分析 → 薄弱点识别 → 下周建议 |
| Mode 9: 健康诊断 | "检查学习健康度" | 遗忘风险检测 → 领域偏科 → 笔记堆积 |

### 三档执行深度

Mode 1 支持三档深度，控制 token 消耗：

| 深度 | 触发方式 | 内容范围 | Token 量 |
|------|---------|---------|---------|
| light | "轻量模式，总结今天学的" | 知识点 + 卡片 | ~2K |
| standard | "总结今天学的"（默认） | 笔记 + 陷阱 + 索引 | ~5K |
| deep | "深度模式，总结今天学的" | 全量 + 资源搜索 | ~10K |

也可在 `config.yaml` 里改默认档位，或让 `analyze-session.py` 自动判断。

## 与其它学习方式的对比

| 维度 | vibe-coding-learning | 手写笔记/Notion | 直接问 AI Chat | Anki/闪卡类 |
|------|---------------------|----------------|---------------|------------|
| 知识来源 | 自动从你的代码中提取 | 需要手动总结 | 需要你自己提问 | 需要手动制卡 |
| 代码关联 | ✅ 精确到文件和行号 | ❌ 脱节 | ⚠️ 通用回答 | ❌ 无关联 |
| 进度追踪 | ✅ 自动统计 | 手动维护 | ❌ 无 | ✅ 间隔复习 |
| 面试准备 | ✅ 基于你的真实项目 | ❌ 需要额外准备 | ⚠️ 通用话术 | ❌ 不适用 |
| 持续成本 | 零（编码后自动触发） | 每次 10-30 分钟 | 每次提问 | 每次制卡 |

## 使用场景

### 场景 1：刚做完一个登录注册模块

```
你：帮我总结今天学的
Skill：→ 自动扫描变更文件 → 提取 JWT、bcrypt、RESTful 等 6 个知识点
      → 逐段讲解 auth.py 的认证逻辑 → 标记 3 个常见陷阱
      → 生成学习笔记 → 更新日历
      → "需要我把核心知识点生成卡片保存吗？"
```

### 场景 2：一周前学的 React Hooks 忘了

```
你：复习一下之前的 React Hooks
Skill：→ 从 topics/ 读取历史笔记 → 先让你自己回忆 useState 和 useEffect 的用法
      → 再揭晓正确答案 → 标记你卡壳的知识点 → 建议再次练习
```

### 场景 3：学期末想看看这学期学了什么

```
你：看看我的学习进度
Skill：→ 读取 progress.md → 展示：3 个领域、42 个知识点、5 个项目
      → 后端 70% ███████░░░ | 前端 45% ████░░░░░░ | AI 30% ███░░░░░░░
      → "前端偏低，建议做个 React 项目补一下"
```

### 场景 4：收到腾讯实习面试通知

```
你：帮我准备前端实习面试
Skill：→ 扫描 topics/ 和 cards/ → 找到你做的登录页、状态管理、响应式布局
      → 生成 30 秒自我介绍："我用纯 HTML/CSS/JS 实现过登录注册模块..."
      → 列出 5 个高频面试题 → "想试一下模拟面试吗？"
```

### 场景 5：一个月做了多个项目，想知道知识怎么串起来

```
你：做一个学习总览
Skill：→ 跨 topic 扫描 → 发现 backend-auth/ 和 frontend-auth/ 都涉及 JWT
      → 自动建立关联："你的 JWT 知识横跨 2 个项目，已生成跨项目知识卡片"
      → 更新 domains/backend/ 索引，标注掌握程度
```

## 项目结构

```
skills/vibe-coding-learning/       # Skill 核心（22 个文件）
├── SKILL.md                        # 主入口（9 个模式 + 三档深度 + 执行策略）
├── config.yaml                     # 配置层（深度/语言/专注领域/复习间隔等）
│
├── references/                     # 参考手册（渐进式加载，按需读取）
│   ├── mode-routing.md              # 意图→模式路由规则
│   ├── output-routing.md            # 输出后续分流规则
│   ├── interview-prep.md            # Mode 4 面试详细流程
│   ├── inbox-triage.md              # Mode 6 知识生命周期管理
│   ├── connection-review.md         # Mode 7 知识关联
│   ├── weekly-synthesis.md          # Mode 8 深度周总结
│   ├── health-check.md              # Mode 9 健康诊断
│   ├── knowledge-taxonomy.md        # 9 领域技术分类体系
│   ├── memory-management.md         # 三层记忆归档策略
│   ├── tutorial-recommendation.md   # 教程搜索词库
│   ├── output-templates.md          # 产出物格式规范
│   ├── test-cases.md                # 测试用例集（10应+5不应+3边界）
│   └── examples/                    # 三份完整示例笔记
│       ├── example-backend-auth.md
│       ├── example-frontend-login.md
│       └── example-agent-langgraph.md
│
├── scripts/                        # 确定性脚本（不依赖 AI 判断）
│   ├── validate-structure.py        # 目录结构校验（7 个检查项）
│   └── analyze-session.py          # 会话复杂度分析（推荐深度档位）
│
└── templates/                      # 输出模板骨架
    ├── daily-learning-note.md
    ├── knowledge-point.md
    └── learning-calendar.md

examples/                           # 配套示例项目（独立可运行）

demo-output/                        # Skill 输出效果演示

learning-notes/                     # 用户本地学习数据（.gitignore）
```

### 加载层级

| 层级 | 内容 | 加载时机 |
|------|------|---------|
| L1（始终加载） | SKILL.md + config.yaml | Skill 触发时立刻读 |
| L2（按需加载） | references/ 对应文件 | 模式确定后只读那一个 |
| L3（工具调用） | scripts/ + templates/ | AI 判断需要确定性验证时 |

## 许可证

MIT
