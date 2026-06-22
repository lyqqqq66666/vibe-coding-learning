# 贡献指南

感谢你对 vibe-coding-learning 的关注！无论是提建议、报 bug 还是贡献代码，都欢迎。

---

## 如何反馈

### 报 Bug

在 [GitHub Issues](https://github.com/lyqqqq66666/vibe-coding-learning/issues/new?template=bug_report.yml) 提交，使用 Bug 反馈模板。

请包含：
- 你使用的 AI 工具（WorkBuddy / Claude Code / Trae 等）
- 你的输入语句
- 预期行为 vs 实际行为

### 提功能建议

在 [GitHub Issues](https://github.com/lyqqqq66666/vibe-coding-learning/issues/new?template=feature_request.yml) 提交，使用功能建议模板。

请描述：
- 你遇到了什么问题（当前 Skill 无法满足的场景）
- 你希望怎么解决
- 有没有其他工具已经实现了类似功能（贴链接）

### 体验反馈

在 [GitHub Issues](https://github.com/lyqqqq66666/vibe-coding-learning/issues/new?template=experience_feedback.yml) 提交，使用体验反馈模板。

随便写感受就行，整体评分 + 使用场景即可。

---

## 如何贡献代码

1. Fork 仓库
2. 在 `dev` 分支上工作
3. 修改后跑一遍 `TESTING.md` 的测试流程
4. 提交 PR 到 `dev` 分支

### 提交信息规范

```
<type>: <简述>

type 取值：
  feat      — 新功能（如新增 Mode）
  fix       — Bug 修复
  docs      — 文档修改（SKILL.md、README、参考手册）
  refactor  — 重构，不改功能
  chore     — 构建、脚本、配置
```

### 文件组织约定

```
skills/vibe-coding-learning/       # Skill 核心（不要随意移动）
├── SKILL.md                        # 主入口
├── config.yaml                     # 配置层
├── references/                     # 参考手册（长内容外移）
├── scripts/                        # 校验和分析脚本
└── templates/                      # 输出模板
```

**注意**：
- 不要在 SKILL.md 中硬编码文件路径
- 新增 references/ 文件后，更新 SKILL.md 的引用说明
- `learning-notes/` 已在 `.gitignore`，不要提交用户数据

---

## 版本迭代

详见 [VERSION-STRATEGY.md](./VERSION-STRATEGY.md)。

- Bug 修复 → PATCH 版本（随时）
- 功能新增 → MINOR 版本（每 2-4 周）
- 架构改动 → MAJOR 版本（按需）

---

## 测试

跑一遍 [TESTING.md](./TESTING.md) 的流程，覆盖所有 9 个模式 + 三档深度 + 状态机闭环。

核心验收标准：
- 应触发：10/10 正确路由
- 不应触发：5/5 不触发
- 边界：3/3 正确澄清
