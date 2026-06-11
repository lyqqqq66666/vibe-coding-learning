# 知识点卡片：bcrypt 密码哈希

## 一句话定义
bcrypt 是一种专门用于密码存储的安全哈希算法，自带随机盐和可调计算成本，能有效抵御暴力破解和彩虹表攻击。

## 核心原理
- 基于 Blowfish 加密算法，设计初衷就是用于密码存储
- 每次哈希自动生成不同的盐（salt），相同密码每次得到的哈希值不同
- 计算成本可调（cost factor），可以随着硬件升级而增加计算时间
- **单向函数**：无法从哈希值反推出原始密码

## Python 用法

```python
import bcrypt

# 哈希密码
hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# 验证密码
is_valid = bcrypt.checkpw(plain_password.encode("utf-8"), hashed.encode("utf-8"))
```

## 关键注意点
- bcrypt 输入输出是 `bytes` 类型，需要 `.encode()` / `.decode()`
- 密码最大长度 72 字节，超出部分会被截断
- passlib 和新版 bcrypt（>=4.1）存在兼容性问题，建议直接用 bcrypt 库

## 常见错误
- 明文存储密码
- 用 MD5/SHA-1 代替 bcrypt（没有盐，计算太快）
- 混用 passlib 和新版 bcrypt 导致报错

## 相关文件
- `fastapi-auth/auth.py` 第 26-33 行
