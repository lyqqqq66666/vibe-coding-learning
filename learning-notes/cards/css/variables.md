     # CSS 自定义属性（CSS Variables）

> 知识卡片 — 可跨主题复用
> 标签：`css` `前端基础` `设计规范`

---

## 是什么

CSS 自定义属性（CSS Variables / CSS Custom Properties）允许在 `:root` 选择器中定义可复用的值，通过 `var(--name)` 在任何 CSS 规则中引用。修改一处，全局生效。

## 核心原理

1. 在 `:root` 中用 `--varname: value` 定义
2. 在任意位置用 `var(--varname)` 引用
3. 浏览器在渲染时替换变量值为实际值
4. 变量值可以被子元素继承，也可以被覆盖

```css
:root {
  --primary: #4f46e5;
  --radius: 12px;
}

.btn {
  background: var(--primary);
  border-radius: var(--radius);
}
```

## 常见用法

- **主题换肤**：定义 `--bg`、`--text`、`--primary`，切换时只需改一组变量
- **统一规范**：圆角 `--radius`、间距 `--gap`、阴影 `--shadow` 统一管理
- **响应式**：在 `@media` 中覆盖变量值适配不同屏幕

## 易错点

- 变量名大小写敏感，`--MainColor` 和 `--mainColor` 是两个变量
- 不能在 `var()` 中做数学运算（如 `var(--gap) * 2`），要用 `calc(var(--gap) * 2)`
- 变量的作用域遵循 CSS 层叠规则，定义在越内层优先级越高

## 相关知识点

- SASS/LESS 变量（编译时）← CSS 变量（运行时）
- CSS @property

---

*首次提取：2026-06-11 | 项目：frontend-auth*
