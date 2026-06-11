# 编程技术知识分类体系 (Knowledge Taxonomy)

> 基于 roadmap.sh 72 个路线图 + SFIA 标准分类。AI 扫描代码时对照此表确定领域、栈和知识点维度。
> 当遇到未覆盖的新技术时，按"归属领域 + 类比现有栈"原则扩展。

---

## 一、领域分类速查

### 1. 后端开发 (backend)

| 子领域 | 代表技术 | 识别特征（代码/文件） |
|--------|---------|---------------------|
| **Python Web** | FastAPI, Django, Flask | `@app.route`, `APIRouter`, `from fastapi import` |
| **Java 企业** | Spring Boot, Spring MVC | `@SpringBootApplication`, `@RestController`, `pom.xml` |
| **Node.js** | Express, NestJS, Koa | `require('express')`, `@Module()`, `package.json` |
| **Go** | Gin, Echo, Fiber | `gin.Default()`, `go.mod`, `func main()` |
| **C#/.NET** | ASP.NET Core, Blazor | `[ApiController]`, `.csproj`, `builder.Services.AddControllers()` |
| **PHP** | Laravel, Symfony | `Route::get`, `php artisan`, `composer.json` |
| **Rust** | Actix, Rocket, Axum | `#[actix_web::main]`, `Cargo.toml` |
| **Ruby** | Rails, Sinatra | `Rails.application.routes`, `Gemfile` |

**知识点提取维度**：
- API 设计（RESTful / GraphQL / gRPC）、路由、中间件
- 数据库交互（ORM / 原生 SQL / 连接池）
- 认证与授权（JWT / OAuth2 / Session / RBAC）
- 输入校验、错误处理、日志、性能优化

---

### 2. 前端开发 (frontend)

| 子领域 | 代表技术 | 识别特征 |
|--------|---------|---------|
| **基础三件套** | HTML5, CSS3, JavaScript | `.html`, `<script>`, `<style>`, `document.querySelector` |
| **React 生态** | React, Next.js, Remix | `import React`, `useState`, `jsx`, `next.config.js` |
| **Vue 生态** | Vue 3, Nuxt.js | `<template>`, `ref()`, `createApp`, `nuxt.config.ts` |
| **Angular** | Angular | `@Component`, `@NgModule`, `angular.json` |
| **TypeScript** | TS 类型系统 | `.ts`, `.tsx`, `interface`, `type`, `enum` |
| **状态管理** | Redux, Zustand, Pinia, Vuex | `createStore`, `createSlice`, `defineStore` |
| **CSS 方案** | Tailwind, Sass, CSS Modules | `tailwind.config`, `.scss`, `.module.css` |
| **构建工具** | Vite, Webpack, Turbopack | `vite.config.ts`, `webpack.config.js` |
| **跨平台** | React Native, Flutter, Taro | `react-native`, `flutter`, `@tarojs/taro` |

**知识点提取维度**：
- 组件设计、Hooks/组合式 API、生命周期
- 响应式布局、CSS 动画、性能优化
- 路由、状态管理、表单处理
- 前端安全（XSS/CSRF）、跨域（CORS）

---

### 3. 数据库 (database)

| 子领域 | 代表技术 | 识别特征 |
|--------|---------|---------|
| **关系型** | PostgreSQL, MySQL, SQLite | `.sql`, `SELECT`, `CREATE TABLE`, `psycopg2`, `sqlalchemy` |
| **NoSQL 文档** | MongoDB | `db.collection.find()`, `mongoose`, `_id` |
| **NoSQL KV** | Redis | `redis.set()`, `redis://`, `REDIS_URL` |
| **NoSQL 搜索** | Elasticsearch | `elasticsearch`, `_search`, `ES_HOST` |
| **ORMs** | Prisma, SQLAlchemy, TypeORM | `schema.prisma`, `Base.metadata`, `@Entity()` |

**知识点提取维度**：
- 表设计/数据建模、索引、查询优化
- 事务、迁移、备份恢复
- ORM vs 原生 SQL、连接池管理

---

### 4. DevOps (devops)

| 子领域 | 代表技术 | 识别特征 |
|--------|---------|---------|
| **容器化** | Docker | `Dockerfile`, `docker-compose.yml`, `FROM python` |
| **编排** | Kubernetes, Docker Swarm | `k8s/`, `deployment.yaml`, `kubectl` |
| **IaC** | Terraform, Ansible, Pulumi | `.tf`, `playbook.yml`, `main.tf` |
| **CI/CD** | GitHub Actions, GitLab CI, Jenkins | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` |
| **监控** | Prometheus, Grafana, Datadog | `prometheus.yml`, `grafana`, `metrics` |
| **Shell** | Bash, Zsh | `#!/bin/bash`, `.sh`, `Makefile` |

**知识点提取维度**：
- 容器化原理、镜像构建、多阶段构建
- 服务编排、自动扩缩容、Helm Chart
- 流水线设计、自动化测试集成、部署策略

---

### 5. AI / ML 开发 (ai-ml)

| 子领域 | 代表技术 | 识别特征 |
|--------|---------|---------|
| **LLM 应用** | LangChain, LlamaIndex, RAG | `from langchain`, `llama_index`, `vector_store` |
| **AI Agent** | LangGraph, CrewAI, AutoGen | `StateGraph`, `crewai`, `Agent` |
| **MCP** | Model Context Protocol | `mcp/`, `MCP_SERVER`, `mcp.json` |
| **Prompt** | Prompt Engineering | `system_prompt`, `prompt_template` |
| **机器学习** | Scikit-learn, Pandas, NumPy | `sklearn`, `pd.DataFrame`, `np.array` |
| **深度学习** | PyTorch, TensorFlow, JAX | `torch.nn`, `tf.keras`, `jnp` |
| **MLOps** | MLflow, Weights & Biases, Kubeflow | `mlflow`, `wandb`, `kubeflow` |

**知识点提取维度**：
- RAG 架构、Chunking 策略、Embedding
- Agent 工具调用、状态管理、多智能体协作
- 模型训练、微调、评估、部署

---

### 6. 云计算 (cloud)

| 子领域 | 代表技术 | 识别特征 |
|--------|---------|---------|
| **AWS** | EC2, Lambda, S3, RDS | `boto3`, `aws_`, `Amazon` |
| **Serverless** | Cloudflare Workers, Vercel | `wrangler.toml`, `vercel.json` |
| **国内云** | 阿里云, 腾讯云, 华为云 | `aliyun`, `tencentcloud`, `huaweicloud` |

**知识点提取维度**：
- 计算/存储/网络服务、IAM 权限、成本优化
- Serverless 架构、冷启动、边缘计算

---

### 7. 安全 (security)

| 子领域 | 代表技术 | 识别特征 |
|--------|---------|---------|
| **Web 安全** | OWASP Top 10, XSS/CSRF/SQLi | `sanitize`, `escape`, `csrf_token` |
| **认证授权** | OAuth 2.0, JWT, SAML, OIDC | `oauth`, `jwt.encode`, `login_required` |
| **加密** | TLS/SSL, bcrypt, AES | `bcrypt`, `cryptography`, `SSL` |

**知识点提取维度**：
- 常见攻击与防御、安全头配置、CORS 策略
- Token 管理、密码存储、HTTPS 配置

---

### 8. 测试 (testing)

| 子领域 | 代表技术 | 识别特征 |
|--------|---------|---------|
| **单元测试** | Jest, Vitest, Pytest, JUnit | `test_`, `describe(`, `it(`, `expect(` |
| **E2E 测试** | Playwright, Cypress, Selenium | `playwright`, `cy.visit`, `selenium` |
| **性能测试** | k6, JMeter, Locust | `k6`, `jmeter`, `locust` |

**知识点提取维度**：
- 测试金字塔、Mock/Stub/Fixture
- 覆盖率、CI 集成、TDD/BDD

---

## 二、跨领域技术

这些技术可能出现在多个领域中，识别时需要标注所有关联领域：

| 技术 | 关联领域 | 识别特征 |
|------|---------|---------|
| **Git** | 全部 | `.git/`, `git clone`, `commit` |
| **REST API** | 后端 + 前端 | `@app.get`, `fetch()`, `axios` |
| **Docker** | 后端 + DevOps + 云 | `Dockerfile`, `docker-compose.yml` |
| **环境变量** | 全部 | `.env`, `os.getenv`, `process.env` |
| **CI/CD** | DevOps + 全部 | `.github/workflows/` |
| **TypeScript** | 前端 + 后端 | `.ts`, `interface`, `type` |
| **GraphQL** | 后端 + 前端 | `type Query`, `graphql`, `apollo` |

---

## 三、使用规则

AI 扫描代码时的判断流程：

1. **扫描文件扩展名和 imports** → 查表确定领域
2. **一个 session 可能跨多个领域** → 生成多个领域条目
3. **遇到表中没有的技术** → 归到最接近的领域，标记为 "new"
4. **跨领域技术** → 同时记录到所有关联领域
5. **领域+栈 组合** → 用于 `domains/[domain]/[stack]/_index.md` 路径生成

优先级：文件扩展名 > imports/依赖 > 目录名 > 用户描述
