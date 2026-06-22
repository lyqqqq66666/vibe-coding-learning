# vibe-coding-origin — Vibe Coding 的起源与哲学

## 概念起源

"Vibe Coding" 由 Andrej Karpathy 于 2025 年 2 月首次提出。他在社交媒体上描述了一种新的编程方式：

> 不再逐行手写代码，而是用自然语言描述意图，让 AI 生成代码。程序员的角色从"写代码的人"变成了"给 AI 指方向的人"——你不再需要记住语法细节，而是需要理解代码在做什么。

这一概念迅速成为 2025 年开发者社区的热词，Collins 词典将其选为 2025 年度词汇。

## 从 Vibe Coding 到 Agentic Engineering

2026 年 4 月，Karpathy 在 Sequoia AI Ascent 大会上进一步阐述了这一概念的演进：

- **Vibe Coding**（2025 年）：人给方向，AI 写代码，人凭直觉（vibe）判断结果是否正确
- **Agentic Engineering**（2026 年）：人设计系统架构和工具链，AI Agent 自动完成编码、测试、部署的完整循环

核心变化：从"人指挥 AI 写一段代码"到"人设计系统让 AI Agent 自主完成整个工程流程"。但这并不意味着人可以完全放手——**理解**仍然是不可替代的。

## 核心哲学

**"You can outsource your thinking, but not your understanding."**
（你可以外包思考，但不能外包理解。）

这句话是本 Skill 设计的核心理念：

| 维度 | 外包思考（可以） | 不可外包理解（不行） |
|------|----------------|-------------------|
| 写代码 | ✅ AI 可以帮你写 | ❌ 但你必须理解这段代码在做什么 |
| 选方案 | ✅ AI 可以帮你比较 | ❌ 但你必须理解为什么选这个方案 |
| 调 bug | ✅ AI 可以帮你定位 | ❌ 但你必须理解 bug 的根因 |
| 写文档 | ✅ AI 可以帮你生成 | ❌ 但你必须理解系统的整体逻辑 |

**Vibe Coding 的真正风险不是"AI 写错了代码"，而是"你以为你理解了但其实没有"。**

本 Skill 的目的就是把"你以为理解了"变成"你真的理解了"。

## Karpathy 的教育项目推荐

Karpathy 是 AI 教育领域的标杆人物，他的开源项目强调"最小可理解实现"——用最少的代码实现核心原理，让学习者真正理解而不是被复杂工程淹没。

| 项目 | Stars | 核心价值 | 适合谁 |
|------|-------|---------|--------|
| **[nanoGPT](https://github.com/karpathy/nanoGPT)** | 60k+ | 最简 GPT 训练脚本（< 300 行训练 + < 300 行推理） | 想理解 GPT 训练原理的人 |
| **[micrograd](https://github.com/karpathy/micrograd)** | 16k+ | 最简 autograd 引擎（< 150 行），从零理解反向传播 | 想理解深度学习基础的人 |
| **[llama2.c](https://github.com/karpathy/llama2.c)** | 19k+ | 单文件 C 实现 Llama 2 推理（< 800 行） | 想理解 LLM 推理流程的人 |
| **[makemore](https://github.com/karpathy/makemore)** | 2k+ | 字级语言模型系列教程（从 Bigram 到 MLP 到 RNN） | 想系统学 NLP 基础的人 |

> 这些项目都是 MIT License 开源，推荐链接完全合法。

## Learning Philosophy: 为什么"理解"比"记忆"更重要

| 传统学习 | Vibe Coding 学习（本 Skill） |
|---------|---------------------------|
| 记住语法 → 手写代码 | 理解原理 → 用 AI 生成 → 验证理解 |
| 看教程 → 做练习 → 考试 | 做 AI 项目 → 反向提取知识 → 费曼自评 |
| 知识是"学来的" | 知识是"从做中提炼的" |

这和 Karpathy 的 **"literate programming"** 思想一致：代码不应该只是可执行的，还应该是可理解的。他每行代码都配有详细解释，因为他相信理解是学习的终点。

## 与本 Skill 的关系

| Karpathy 的原则 | 本 Skill 的实现 |
|----------------|----------------|
| "外包思考但不能外包理解" | Mode 1 Step 10 费曼自评：写完笔记后反问你是否真的理解 |
| "最小可理解实现" | 知识卡片设计：每张卡片是"最小可理解单元" |
| "literate programming" | 代码讲解：每段代码配"为什么这样设计"解释 |
| "Agentic Engineering" | Mode 5: 分析你和 AI 的协作效率，优化提示词 |
| 教育项目推荐 | 本 Skill Step 6 推荐学习资源，优先官方文档和 B 站 |
