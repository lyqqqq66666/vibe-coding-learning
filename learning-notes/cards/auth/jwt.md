# 知识点卡片：JWT（JSON Web Token）

## 一句话定义
JWT 是一种无状态的令牌认证机制，服务端签发一个包含用户信息的加密字符串，客户端每次请求都携带它来证明身份。

## 结构
JWT 由三部分组成，用 `.` 分隔：

```
Header.Payload.Signature
```

- **Header**：算法类型（如 `HS256`）和 Token 类型
- **Payload**：用户数据（如 `sub` 用户标识、`exp` 过期时间）
- **Signature**：用密钥对前两部分签名，防止篡改

## 工作流程
1. 用户提交用户名密码
2. 服务端验证通过后，用 `SECRET_KEY` 签发 JWT
3. 客户端保存 Token，后续请求在 Header 中携带：`Authorization: Bearer <token>`
4. 服务端收到请求后，用 `SECRET_KEY` 验证 Token 的有效性
5. 验证通过后，从 Token 中提取用户信息

## Python 用法（python-jose）

```python
from jose import jwt

# 生成 Token
token = jwt.encode({"sub": "username", "exp": expire_time}, SECRET_KEY, algorithm="HS256")

# 验证 Token
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
username = payload.get("sub")
```

## 关键注意点
- `SECRET_KEY` 必须保密，泄露则整个认证体系失效
- 务必设置 `exp`（过期时间），不要生成永不过期的 Token
- JWT 是 Base64 编码，不是加密，Payload 中的信息任何人都能看到（不要放密码）
- Token 存在客户端（localStorage 或 cookie），存在 XSS 风险

## 常见错误
- 不设过期时间
- Secret Key 硬编码在代码中
- 在 Payload 中存放敏感信息

## 相关文件
- `fastapi-auth/auth.py` 第 36-62 行
