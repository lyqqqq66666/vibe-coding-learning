# 学习进度总览

> 最后更新：2026-06-11

---

## 统计

| 指标 | 数值 |
|------|------|
| 总学习天数 | 2 |
| 覆盖领域 | 2（后端开发、前端开发） |
| 技术栈 | 2（FastAPI、Vanilla JS） |
| 知识点数量 | 15 |
| 知识卡片 | 8 |

---

## 各领域进度

### 后端开发（Backend Development）

进度：████░░░░░░ 30%

- [x] FastAPI 框架基础
- [x] Pydantic 数据模型
- [x] SQLAlchemy ORM
- [x] bcrypt 密码哈希
- [x] JWT 认证
- [x] 依赖注入（Depends）
- [x] CORS 跨域配置
- [ ] OAuth2 完整授权流程
- [ ] Refresh Token
- [ ] RBAC 角色权限
- [ ] 数据库迁移（Alembic）
- [ ] 单元测试

**技术栈**：
- FastAPI: 7/12 知识点 ([查看详情](./domains/backend/fastapi/_index.md))

---

### 前端开发（Frontend Development）

进度：████░░░░░░ 22%

- [x] HTML5 表单与语义化
- [x] CSS 自定义属性（CSS Variables）
- [x] CSS Flexbox 居中对齐
- [x] CSS 动画（@keyframes + transition）
- [x] CSS 媒体查询响应式
- [x] JavaScript DOM 操作
- [x] 客户端表单校验
- [x] 密码显隐切换
- [ ] CSS Grid 布局
- [ ] Fetch API / AJAX 交互
- [ ] localStorage 持久化
- [ ] ES6+ 模块化
- [ ] 构建工具（Vite）
- [ ] 前端测试（Jest/Vitest）

**技术栈**：
- Vanilla JS: 8/14 知识点 ([查看详情](./domains/frontend/vanilla-js/_index.md))

---

## 最近学习

| 日期 | 主题 | 领域 | 技术栈 |
|------|------|------|--------|
| 2026-06-11 | FastAPI 登录注册后端 | 后端开发 | FastAPI |
| 2026-06-11 | HTML/CSS/JS 登录注册前端 | 前端开发 | Vanilla JS |

---

## 知识卡片库

| 分类 | 卡片数量 | 路径 |
|------|----------|------|
| 认证与安全 | 2 | [./cards/auth/](./cards/auth/) |
| CSS | 3 | [./cards/css/](./cards/css/) |
| JavaScript | 1 | [./cards/js/](./cards/js/) |
| Python | 2 | [./cards/python/](./cards/python/) |

---

## 建议下一步

1. 将前端登录注册对接已有的 FastAPI 后端，实现前后端联调
2. 学习 Alembic 数据库迁移工具
3. 添加 Refresh Token 机制
4. 为 API 编写单元测试
