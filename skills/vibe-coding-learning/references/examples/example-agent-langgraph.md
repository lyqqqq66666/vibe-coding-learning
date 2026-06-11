# 示例：AI Agent — LangGraph 多智能体协作 学习笔记

> 这是 `vibe-coding-learning` Skill 在 AI/ML 领域的示例输出格式。

---

## 基本信息

- **日期**：2026-06-20
- **技术领域**：AI Agent 开发 / LLM 应用
- **AI 工具**：WorkBuddy
- **任务描述**：用 LangGraph 构建了一个多角色协作的写作 Agent（Planner → Writer → Reviewer）

---

## 知识点归纳

### 1. LangGraph 状态图（StateGraph）

- **是什么**：LangGraph 的核心抽象，用有向图定义 Agent 工作流的状态和节点
- **核心原理**：StateGraph → add_node 添加节点 → add_edge 连接边 → compile 编译运行
- **关键代码**：`graph.py` 第 12-28 行

### 2. 条件路由（Conditional Edges）

- **是什么**：根据状态动态决定下一步走哪个节点，实现分支逻辑
- **核心原理**：定义路由函数 → 返回目标节点名 → add_conditional_edges 绑定
- **关键代码**：`graph.py` 第 35-42 行

### 3. Tool Calling（工具调用）

- **是什么**：让 LLM 在对话过程中调用外部函数（搜索、计算、数据库查询等）
- **核心原理**：定义工具函数 + 装饰器 → bind_tools 绑定到 LLM → ToolNode 执行
- **关键代码**：`tools.py` 第 5-20 行

---

## 代码讲解

### 先读哪里

`state.py`（状态定义）→ `tools.py`（工具函数）→ `graph.py`（工作流）→ `main.py`（入口）

### 逐段解读

#### state.py — 状态定义

```python
class AgentState(TypedDict):
    messages: Annotated[List, operator.add]
    plan: str
    draft: str
    review: str
```

- 用 TypedDict 定义状态结构
- `Annotated[List, operator.add]` 实现 append-only 的消息列表
- `plan`/`draft`/`review` 分别存储三个阶段产物

#### graph.py — 工作流

```python
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner_node)
workflow.add_node("writer", writer_node)
workflow.add_node("reviewer", reviewer_node)
workflow.add_edge("planner", "writer")
workflow.add_conditional_edges("reviewer", decide_next, {
    "approve": END,
    "revise": "writer"
})
```

- 三个角色节点串联
- Reviewer 判断后决定通过还是打回重写
- 实现了人类写作中的"审稿-修改"循环

### 为什么这样设计

- **为什么用 StateGraph？** 比 Chain 更灵活，支持条件和循环
- **为什么三个角色分开？** 单一职责：规划/执行/审查分离，输出质量更高
- **为什么 Reviewer 可以打回？** 引入质量控制循环，模拟真实的迭代写作流程

---

## 易错点整理

| 易错点 | 正确做法 | 常见错误 |
|--------|---------|---------|
| 消息列表不追加 | `Annotated[List, operator.add]` | 每次覆盖导致对话历史丢失 |
| API Key 硬编码 | `os.getenv("OPENAI_API_KEY")` | 直接写在代码里 |
| Tool 定义无类型提示 | 参数和返回值加类型注解 | LLM 猜不到参数格式 |
| 循环不设退出条件 | `add_conditional_edges` + 最大次数 | 无限循环耗光 token |

---

## 推荐学习资源

1. **[文档] LangGraph 官方教程**
   https://langchain-ai.github.io/langgraph/tutorials/

2. **[B站] LangGraph Agent 开发实战**
   搜索关键词：LangGraph Agent 多智能体

3. **[博客] 用 LangGraph 构建多角色协作 Agent**
   https://blog.langchain.dev/langgraph-multi-agent/

---

## 下一步学习建议

- [ ] 添加 Checkpointer 实现对话持久化
- [ ] 引入 Human-in-the-loop（人工审核节点）
- [ ] 尝试用 CrewAI 实现相同场景，对比两个框架
