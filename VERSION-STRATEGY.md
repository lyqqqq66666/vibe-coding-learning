# vibe-coding-learning 版本迭代策略

> 公开发布后的反馈收集、版本管理、迭代节奏

---

## 版本号规范

遵循 SemVer（语义化版本）：

```
MAJOR.MINOR.PATCH

MAJOR — 架构级改动（新增 Mode、重构核心流程）
MINOR — 功能优化（新配置项、脚本升级、参考手册更新）
PATCH — Bug 修复、文案修正、格式调整
```

当前版本：`1.1.0`

---

## 反馈来源与分类

| 来源 | 收集方式 | 处理节奏 |
|------|---------|---------|
| GitHub Issues | `.github/ISSUE_TEMPLATE/` 三类模板 | 每周 review |
| 直接对话反馈 | 用户在 AI 工具里说的建议 | 随时记录到 Issues |
| 社交媒体/论坛 | 腾讯云开发者社区等 | 每两周扫描 |
| 自测发现 | TESTING.md 跑完后的遗漏 | 即时修复 |

---

## 反馈处理流程

```
用户提交 Issue
      ↓
分类：bug / feature / feedback
      ↓
Bug → 立刻修 → PATCH 版本
Feature → 评估优先级 → 加入待办 → 下一个 MINOR 版本
Feedback → 分析共性 → 可能转 feature 或优化 → 下一个 MINOR 版本
      ↓
修复/实现 → dev 分支测试 → 合并到 main → 推送触发同步
```

---

## 优先级评估矩阵

| 优先级 | 条件 | 示例 |
|--------|------|------|
| P0（紧急） | 多人反馈的 bug 或模式路由错误 | Mode 1 误触发到 Mode 5 |
| P1（高） | 单人 bug + 功能请求 ≥ 3 人点赞 | "希望加自动遗漏检测" |
| P2（中） | 体验优化 + 明确场景 | "输出格式更紧凑" |
| P3（低） | 锦上添花 + 暂无实际用户 | "加 assets 目录放图标" |

---

## 发布节奏

| 类型 | 频率 | 分支 |
|------|------|------|
| PATCH（热修） | 随时，发现问题即修 | dev → main |
| MINOR（功能版） | 每 2-4 周 | dev → main |
| MAJOR（架构版） | 按需，有重大改动时 | dev → 充分测试 → main |

---

## 变更日志模板

每次发布在 `CHANGELOG.md` 中记录：

```markdown
## [1.2.0] - 2026-07-XX

### Added
- Mode 10：自动遗漏检测

### Changed
- Mode 1 light 档现在也写入 frontmatter
- config.yaml 新增 `learning.auto_depth: true` 选项

### Fixed
- Mode 5 误触发到 Mode 1 的问题 (#12)
- validate-structure.py 无法检测嵌套目录的问题 (#8)

### Deprecated
- Mode 3 简单统计将被 Mode 8 weekly-synthesis 替代（v2.0 移除）
```

---

## 用户通知机制

| 事件 | 通知方式 |
|------|---------|
| 新版本发布 | GitHub Release + README 版本号更新 |
| 重要 bug 修复 | Issue 评论通知 + Release notes |
| 功能变更 | CHANGELOG.md + README 更新说明 |
| Breaking Change | Issue 提前公告 + README 迁移指南 |

---

## 测试覆盖率目标

| 版本阶段 | 测试覆盖率 |
|---------|-----------|
| v1.x（当前） | 应触发 10/10 + 不应触发 5/5 + 边界 3/3 |
| v2.0（架构版） | 每个模式至少 3 个独立测试场景 |
| v3.0+ | 自动化 E2E 测试（CI 集成） |
