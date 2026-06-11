     # CSS 动画（@keyframes + transition）

> 知识卡片 — 可跨主题复用
> 标签：`css` `动画` `前端基础`

---

## 是什么

CSS 提供两种动画机制：`transition` 实现属性值变化时的平滑过渡，`@keyframes` 定义多阶段自定义动画。

## 核心原理

**transition**（过渡动画）：
```css
.btn {
  transform: scale(1);
  transition: transform 0.15s ease;
}
.btn:hover {
  transform: scale(1.05);  /* 0.15 秒内平滑放大 */
}
```
- 需要状态变化触发（hover、focus、class 切换等）
- 四要素：属性名、时长、缓动函数、延迟

**@keyframes**（关键帧动画）：
```css
@keyframes slideIn {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}
.card {
  animation: slideIn 0.5s ease;
}
```
- 加载即播放，不需要状态触发
- 可以定义 0% ~ 100% 任意阶段的样式

## 重新触发动画的 trick

```javascript
el.style.animation = "none";
void el.offsetWidth;  // 强制浏览器重排
el.style.animation = "";
```

先清除再恢复，让浏览器忘掉之前的动画状态。

## 易错点

- `transition` 写在元素默认状态上，不能写在 `:hover` 里（否则只有 enter 有动画，leave 没有）
- `animation` 不会重复播放，需要清除再恢复
- 动画过多会卡顿，优先用 `transform` 和 `opacity`（不触发重排）

---

*首次提取：2026-06-11 | 项目：frontend-auth*
