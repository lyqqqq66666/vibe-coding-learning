# 示例：前端登录注册 — HTML/CSS/JS 学习笔记

> 这是 `vibe-coding-learning` Skill 生成的前端学习笔记示例。

---

## 基本信息

- **日期**：2026-06-11
- **技术领域**：前端开发 / Web 交互 / 表单校验
- **AI 工具**：WorkBuddy
- **任务描述**：用纯 HTML/CSS/JS 实现了登录注册前端页面

---

## 知识点归纳

### 1. CSS 自定义属性（CSS Variables）

- **是什么**：在 `:root` 中定义可复用值，统一管理颜色、间距、圆角等
- **核心原理**：`--primary: #4f46e5` 定义 → `var(--primary)` 引用 → 改一处全局生效
- **关键代码**：`index.html` 第 20-30 行

### 2. Flexbox 居中布局

- **是什么**：CSS3 一维弹性盒模型，通过主轴和交叉轴对齐子元素
- **核心原理**：`display: flex` + `align-items: center` + `justify-content: center`
- **关键代码**：`index.html` 第 36-42 行

### 3. 客户端表单校验

- **是什么**：提交前用 JS 验证输入格式，即时反馈，避免无效请求
- **核心原理**：正则校验邮箱 → 长度校验密码 → `===` 比较确认密码 → 返回 true/false
- **关键代码**：`index.html` 第 282-327 行

---

## 代码讲解

### 先读哪里

HTML 结构 → CSS `:root` 变量 → Flexbox 布局 → JS 校验 → JS 事件绑定

### 逐段解读

#### HTML 表单结构

```html
<form id="login-form" novalidate>
  <input type="email" id="login-email" placeholder="请输入邮箱">
  <input type="password" id="login-password" placeholder="请输入密码">
  <button type="button" class="toggle-pwd">👁</button>
</form>
```

- `novalidate` 关闭浏览器默认校验，改 JS 控制
- `type="email"` 移动端弹出邮箱键盘
- 密码眼按钮 `type="button"` 防止误触发表单提交

#### CSS 动画

```css
@keyframes cardIn {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

- `transform` 和 `opacity` 不触发重排，性能最优
- 重新播放需清除再恢复：`void element.offsetWidth` 强制重排

### 为什么这样设计

- **为什么不用框架？** 需求简单，零构建步骤，学习阶段先理解原生 API
- **为什么 CSS 和 JS 写在一个文件？** 降低认知负担，学完再拆
- **为什么校验放前端？** 即时反馈用户体验好；但不能替代后端校验

---

## 易错点整理

| 易错点 | 正确做法 | 常见错误 |
|--------|---------|---------|
| 按钮默认提交 | `type="button"` | 忘加导致点眼图标触发表单提交 |
| CSS 动画不重播 | 清除 `animation` → `void offsetWidth` → 恢复 | 以为改 class 就能重新播 |
| 正则不锚定 | `^...$` 首尾锚定 | `/@.+\..+/` 部分匹配就通过 |
| 只做前端校验 | 前后端都校验 | 认为前端够用，后端可绕过 |

---

## 推荐学习资源

1. **[MDN] 表单数据校验**
   https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Extensions/Forms/Form_validation

2. **[B站] 登录注册页面实战**
   搜索关键词：HTML CSS 登录注册 实战

3. **[教程] JS 表单验证完整方案**
   https://blog.csdn.net/weixin_42594427/article/details/152539686

---

## 下一步学习建议

- [ ] 拆 CSS/JS 到独立文件，引入 Vite
- [ ] 对接 FastAPI 后端实现真实登录
- [ ] 学习 React 重构同一页面
