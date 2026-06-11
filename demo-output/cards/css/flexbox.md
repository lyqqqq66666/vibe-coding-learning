     # CSS Flexbox 居中对齐

> 知识卡片 — 可跨主题复用
> 标签：`css` `布局` `前端基础`

---

## 是什么

Flexbox（弹性盒布局）是 CSS3 引入的一维布局系统，通过 `display: flex` 创建弹性容器，用主轴和交叉轴控制子元素的排列和对齐方式。

## 核心原理

```css
.container {
  display: flex;
  justify-content: center;  /* 主轴方向（默认水平）居中 */
  align-items: center;      /* 交叉轴方向（默认垂直）居中 */
}
```

- **弹性容器**（flex container）：设置了 `display: flex` 的父元素
- **弹性项目**（flex items）：容器内的直接子元素
- **主轴**：`flex-direction` 决定（默认 `row`，水平方向）
- **交叉轴**：垂直于主轴的方向

## 常见用法

- 页面居中：`body { display: flex; align-items: center; justify-content: center; min-height: 100vh; }`
- 导航栏：`nav { display: flex; justify-content: space-between; align-items: center; }`
- 卡片列表：`flex-wrap: wrap` + `gap: 16px`

## 易错点

- `align-items` 和 `align-content` 容易混淆——前者管单行内对齐，后者管多行之间对齐
- 容器需要显式高度，否则 `align-items: center` 看不出效果
- Flexbox 是一维布局，多维布局用 Grid

## 相关知识点

- CSS Grid 布局
- `position: absolute` + `transform` 居中（旧方法）

---

*首次提取：2026-06-11 | 项目：frontend-auth*
