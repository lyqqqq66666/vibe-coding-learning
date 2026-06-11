# 学习笔记

> 用 AI 编码时，别忘了把学到的知识沉淀下来。

---

## 目录结构

```
learning-notes/
├── README.md                    # 本文件 — 使用说明与总览
├── progress.md                  # 学习进度总览
├── calendar/                    # 按月记录学习日历
│   └── 2026-06.md
├── topics/                      # 按项目/会话组织的笔记
│   ├── fastapi-login-register/
│   │   └── 2026-06-11-fastapi-login-register.md
│   └── html-css-js-login-register/
│       └── 2026-06-11-html-css-js-login-register.md
├── domains/                     # 按技术领域组织的索引
│   ├── backend/
│   │   ├── _index.md
│   │   └── fastapi/
│   │       └── _index.md
│   └── frontend/
│       ├── _index.md
│       └── vanilla-js/
│           └── _index.md
└── cards/                       # 可复用的知识卡片（按技术分类）
    ├── auth/
    │   ├── bcrypt.md
    │   └── jwt.md
    ├── css/
    │   ├── animation.md
    │   ├── flexbox.md
    │   └── variables.md
    ├── js/
    │   └── form-validation.md
    └── python/
        ├── fastapi-depends.md
        └── sqlalchemy.md
```

## 三层组织说明

| 层级 | 用途 | 示例 |
|------|------|------|
| **topics/** | 按项目/会话保存原始学习笔记 | `fastapi-login-register/` |
| **domains/** | 按技术领域建立索引和知识清单 | `backend/fastapi/` |
| **cards/** | 可跨主题复用的知识点卡片 | `auth/jwt.md` |

## 使用方式

- 完成一次编码后，说 **"总结今天的学习"**
- 想复习时，说 **"帮我复习之前的笔记"**
- 想了解进度时，说 **"我的学习进度怎么样"**

## 扩展指南

当你学习新技术时：

1. **新增技术领域**：在 `domains/` 下创建新目录，如 `domains/devops/`
2. **新增技术栈**：在对应领域下创建子目录，如 `domains/devops/docker/`
3. **新增知识卡片**：在 `cards/` 下找到对应分类，或创建新分类
4. **新增会话笔记**：在 `topics/` 下创建项目文件夹
