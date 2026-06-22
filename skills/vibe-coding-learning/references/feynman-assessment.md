# feynman-assessment — 费曼自评环节

## 核心理念

**"你可以外包思考，但不能外包理解。"** — Andrej Karpathy

笔记写完 ≠ 知识掌握。费曼学习法的精髓是：**如果你不能用简单的话把一个概念讲给别人听，你就还没真正理解它。**

本环节在 Mode 1 standard/deep 模式结束后触发，形成"提取 → 整理 → 自评 → 调整掌握度"的学习闭环。

## 触发条件

| 条件 | 触发 |
|------|------|
| `config.yaml` 中 `learning.feynman_enabled: true` | ✅ 触发 |
| `learning.feynman_enabled: false` | ❌ 不触发，直接结束 |
| 用户在对话中说"跳过自评" | ❌ 不触发 |

## 执行步骤

### Step 1 — 列出知识点让用户选择

输出格式：

```
📝 费曼自评时间！

刚才提取了以下知识点，请告诉我：

**哪个知识点你最不熟悉？**（选 1-2 个）
1. {{KNOWLEDGE_POINT_1}} — {{ONE_LINE_DEF}}
2. {{KNOWLEDGE_POINT_2}} — {{ONE_LINE_DEF}}
3. {{KNOWLEDGE_POINT_3}} — {{ONE_LINE_DEF}}
...
N. {{KNOWLEDGE_POINT_N}} — {{ONE_LINE_DEF}}

或者直接说"全部熟悉"跳过自评。
```

### Step 2 — 根据用户回答调整掌握度

| 用户回答 | 操作 |
|---------|------|
| "第 X 个最陌生" | 将该知识点 mastery_level 从 `🟡 understood` 或 `🟢 mastered` 降级为 `🔴 exposed` |
| "第 X 和 Y 都不熟" | 同时降级两个知识点 |
| "全部熟悉" | 不调整，保持原 mastery_level |
| "第 X 个我能给别人讲" | 将该知识点升级为 `🟢🟢 teachable`（最高掌握层级） |

### Step 3 — 推进后续分流

根据自评结果，给出下一步建议：

| 自评结果 | 建议下一步 |
|---------|-----------|
| 有 🔴 exposed 知识点 | "建议对 `[知识点名]` 做 Mode 2 互动复习" |
| 有 🟢🟢 teachable 知识点 | "你已能讲清楚 `[知识点名]`，可以跳过复习了" |
| 全部 🟢 mastered | "这组知识点掌握良好，建议挑战进阶内容" |

## 与其它 Mode 的联动

- **Mode 2（互动复习）**：费曼自评标记的 🔴 知识点是 Mode 2 的优先复习对象
- **Mode 3（学习进度）**：自评结果会影响 mastery ratio 计算
- **Mode 4（面试准备）**：🔴 知识点会被优先出面试题
- **Mode 8（周总结）**：teachable 级知识点会被标注为"优势项"

## 掌握度四级体系

| 级别 | 标记 | 含义 | 到达方式 |
|------|------|------|---------|
| 🔴 exposed | 接触过 | 见过但还不会用，或自评标记为"陌生" | M1 初次创建 / 费曼自评降级 |
| 🟡 understood | 理解了 | 知道怎么用但还不能脱离代码 | M1 默认 / 复习后晋升 |
| 🟢 mastered | 已掌握 | 能不看代码讲清楚原理 | 复习多次后晋升 |
| 🟢🟢 teachable | 可教学 | 能给别人讲清楚，举出例子和类比 | 费曼自评用户主动标记 |

## 配置项

```yaml
learning:
  feynman_enabled: true   # 是否在 M1 结束后触发费曼自评
  feynman_min_points: 3   # 知识点少于此数量时不触发自评（太少没意义）
```
