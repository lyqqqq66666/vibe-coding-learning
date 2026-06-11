# AGENTS.md — AI Agent 协作规范

> vibe-coding-learning 项目的双 Agent 协作约定。Codex 和 WorkBuddy 均可直接读取。

## Agent 分工

| 维度 | Codex | WorkBuddy |
|------|-------|-----------|
| **核心职责** | 前端 / 样式 / 文案 | 后端逻辑 / 架构 / 测试 |
| **本项目角色** | README 打磨、HTML 模板美化、前端示例 | SKILL.md 架构、references/ 逻辑、工程化 |
| **擅长领域** | CSS、HTML、响应式、视觉设计 | Python、工作流设计、Git 管理、文档结构 |
| **不擅长的** | 后端逻辑、数据库设计 | 精细化前端样式 |

## 分支策略

```
main ← 发布分支（稳定，可被用户 git clone 使用）
  ↑  merge via PR
dev  ← 开发分支（日常所有改动在这里）
```

- **dev**：日常开发。新增功能、修复、文档改进都在 dev 上做。
- **main**：稳定版本。dev 上一轮迭代确认无误后合并到 main。

## 提交信息规范

```
<type>: <简述>

type 取值：
  feat      — 新功能
  docs      — 文档修改（README、DESIGN.md 等）
  refactor  — 重构，不改功能
  fix       — 修复 bug
  chore     — 构建、依赖、工具配置
```

示例：
```
feat: add execution strategy layer to SKILL.md
docs: add comparison table to README
refactor: reorganize references/ directory
```

## 文件组织约定

```
skills/vibe-coding-learning/       # Skill 核心（不可随意移动）
├── SKILL.md                        # 主入口，Codex 也可直接读取执行
├── references/                     # 参考手册
├── templates/                      # 输出模板

learning-notes/                    # 用户本地学习数据（gitignore）

examples/                          # 配套示例项目（独立可运行）

demo-output/                       # Skill 效果演示
```

## 开发流程

1. 在 `dev` 分支上工作
2. 改完一组相关文件后，立即 commit
3. 如果有 README 修改，Codex 负责润色后 WorkBuddy review
4. 如果有 SKILL.md 修改，WorkBuddy 负责架构后 Codex review 文案

## 注意事项

- `learning-notes/` 已在 `.gitignore`，不要提交用户数据
- 不要在 SKILL.md 中硬编码具体的文件路径（使用相对路径和约定）
- 新增 references/ 或 templates/ 文件后，更新 SKILL.md 中的引用说明
