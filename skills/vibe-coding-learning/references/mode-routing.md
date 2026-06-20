# Mode Routing — 意图识别与模式路由

> 本文件定义用户输入 → 意图标签 → 执行模式的完整映射规则。
> SKILL.md 主文件通过引用本文件保持简洁。

---

## 意图识别规则

根据用户输入的第一个自然语言指令，按以下优先级识别意图：

### 优先级 1：显式关键词匹配

| 关键词组 | 识别意图 | 路由模式 |
|-----------|----------|----------|
| 总结、整理、学了什么、今天学的 | `quick_summary` | Mode 1 |
| 讲一下、为什么、怎么理解、这段代码 | `guided_learning` | Mode 1（Collaborative） |
| 深入理解、原理、对比、替代方案 | `deep_explanation` | Mode 1（Collaborative） |
| 复习、回顾、之前学的、昨天 | `review_recall` | Mode 2 |
| 进度、学了多少、学习情况、掌握 | `progress_check` | Mode 3 |
| 面试、准备面试、模拟面试、面试怎么讲 | `interview_prep` | Mode 4 |
| 提示词、prompt、怎么问、优化提问 | `prompt_review` | Mode 5 |
| inbox、待整理、批处理、未归档 | `inbox_triage` | Mode 6 |
| 关联、建立链接、知识网络、知识图谱 | `connection_review` | Mode 7 |
| 周总结、本周学习、生成本周报告 | `weekly_synthesis` | Mode 8 |
| 健康度、遗忘、忘记复习、知识诊断 | `health_check` | Mode 9 |

### 优先级 2：模糊表达处理

| 用户输入 | 处理方式 |
|-----------|----------|
| "学习笔记"、"想学东西"、"帮我看看" | 标记为 `ambiguous`，进入 Collaborative 模式，先澄清意图 |
| 只有代码片段，无文字说明 | 询问"你想让我总结这段代码的学习内容，还是讲解代码逻辑？" |
| "随便"、"都可以" | 按默认方案执行（Mode 1 quick summary） |

---

## 模式选择矩阵

| 意图标签 | 触发示例 | 默认模式 | 执行策略 | 输出形式 |
|---------|---------|---------|---------|---------|
| `quick_summary` | "总结今天学的"、"帮我整理今天的代码" | Mode 1 | Auto 直出 | 学习笔记 Markdown |
| `guided_learning` | "这段代码讲一下"、"为什么要这样写" | Mode 1 | Collaborative | 代码讲解 + 追问 |
| `deep_explanation` | "帮我深入理解这个设计模式"、"为什么用 JWT 不用 Session" | Mode 1（深） | Collaborative | 深度讲解 + 替代方案对比 |
| `review_recall` | "复习昨天的"、"之前学过什么" | Mode 2 | Auto 直出 | 测验式复习卡片 |
| `progress_check` | "我学了多少了"、"学习进度怎么样" | Mode 3 | Auto 直出 | 进度仪表盘 |
| `interview_prep` | "帮我准备面试"、"模拟面试" | Mode 4 | Collaborative | 面试话术 + 模拟提问 |
| `prompt_review` | "我的提示词怎么样"、"怎么问才能得到更好回答" | Mode 5 | Collaborative | 提示词分析报告 |
| `inbox_triage` | "有什么没整理的笔记吗"、"整理一下 inbox" | Mode 6 | Collaborative | Inbox 待处理报告 |
| `connection_review` | "今天学的和之前有什么关联"、"帮我建立知识关联" | Mode 7 | Auto 直出 | 知识关联建议 |
| `weekly_synthesis` | "周总结"、"生成本周学习报告" | Mode 8 | Auto 直出 | 深度周总结报告 |
| `health_check` | "检查学习健康度"、"我有没有忘记复习的" | Mode 9 | Auto 直出 | 知识健康诊断报告 |
| `ambiguous` | "学习笔记"、"想学东西" | — | Collaborative，先澄清意图再决定 | 视澄清结果而定 |

---

## 双模式路由详细规则

### Auto 直出模式

**触发条件（满足任一即触发 Auto）**：
- 用户表达明确具体（如"总结今天 FastAPI 的登录代码"）
- 上下文代码变更清晰，学习目标自明
- 用户说"直接做"、"别问了"

**行为**：静默执行全流程，直接输出结果，不提问。

### Collaborative 协作模式

**触发条件（满足任一即触发 Collaborative）**：
- 用户表达模糊宽泛（如"帮我整理学习笔记"）
- 多项目混杂，不确定聚焦哪个
- 意图识别为 `deep_explanation`、`interview_prep`、`prompt_review`
- 用户主动说"帮我规划一下"、"我想先确认"

**行为**：关键节点确认，最多 3 个问题后执行。

---

## 最小提问规则（协作模式遵守）

1. **容量上限**：每次交互最多 3 个关键问题，超过 3 个 → 自行取舍优先级
2. **可推断不提问**：项目名、文件列表、技术栈等能从上下文推断的信息，直接采纳不出声
3. **给出默认值**：需要选择时先给推荐方案并说明理由，让用户一键确认而非从零选择
4. **用户说"直接做"→ 切 Auto**：不再提问，按当前判断执行
5. **默认方案兜底**：如用户犹豫或回复模糊（如"随便""都可以"），直接按推荐方案执行，不再追问

---

## 路由 fallback 逻辑

```
用户输入
   ↓
显式关键词匹配？
   ├─ 是 → 直接路由到对应 Mode
   └─ 否 ↓
模糊表达？
   ├─ 是 → Collaborative 模式，澄清意图
   └─ 否 ↓
上下文有活跃项目？
   ├─ 是 → 假设用户想总结当前项目（Mode 1 Auto）
   └─ 否 ↓
默认 → Mode 1（引导用户提供 coding_context）
```
