# 认证方式变更说明

## 📋 变更概述

**变更时间**: 2025-11-30  
**变更类型**: 认证方式调整  
**影响范围**: 用户登录接口

---

## 🔄 变更内容

### 变更前：企业微信登录
- 使用企业微信 OAuth2.0 授权登录
- 需要配置企业微信应用
- 接口：`POST /auth/wework/login` 和 `GET /auth/wework/auth-url`

### 变更后：用户名密码登录
- 使用传统的用户名密码登录方式
- 无需外部服务依赖
- 接口：`POST /auth/login`

---

## 📝 新接口说明

### 用户登录

**接口**: `POST /api/v1/auth/login`

**请求参数**:
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**错误响应**:
- `401 Unauthorized` - 用户名或密码错误
- `403 Forbidden` - 账号已被封禁

---

## 🗄️ 数据库变更

### User 表结构变更

**删除字段**:
- `openid` - 微信 OpenID
- `wework_userid` - 企业微信 UserID

**新增字段**:
- `username` - 用户名（唯一，必填）
- `password_hash` - 密码哈希（必填）

**保留字段**:
- `device_id` - 设备指纹（可选）
- `is_banned` - 是否被封禁
- `is_admin` - 是否是管理员

---

## 🚀 初始化步骤

### 1. 删除旧数据库（如果存在）

```bash
# 删除旧的数据库文件
rm forest_hole.db
```

### 2. 运行初始化脚本

```bash
cd forest_hole_backend
python init_db.py
```

### 3. 查看创建的账号

初始化脚本会自动创建以下账号：

**管理员账号**:
- 用户名: `admin`
- 密码: `admin123`

**测试账号**:
- 用户名: `testuser1`, `testuser2`, `testuser3`
- 密码: `password123`

---

## 🧪 测试登录

### 使用 curl 测试

```bash
# 登录测试用户
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser1", "password": "password123"}'

# 登录管理员
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 使用 Python 测试

```python
import requests

# 登录
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "username": "testuser1",
        "password": "password123"
    }
)

if response.status_code == 200:
    token = response.json()["access_token"]
    print(f"登录成功！Token: {token}")
    
    # 使用 token 访问其他接口
    headers = {"Authorization": f"Bearer {token}"}
    posts = requests.get(
        "http://localhost:8000/api/v1/posts",
        headers=headers
    )
    print(posts.json())
else:
    print(f"登录失败: {response.json()}")
```

---

## 📚 相关文件变更

### 代码文件

| 文件 | 变更说明 |
|------|----------|
| `app/models/user.py` | 更新用户模型，添加 username 和 password_hash 字段 |
| `app/schemas/user.py` | 更新 Schema，支持用户名密码登录 |
| `app/api/v1/auth.py` | 重写认证接口为用户名密码登录 |
| `app/core/security.py` | 添加密码验证和哈希函数 |
| `app/core/config.py` | 删除企业微信配置项 |
| `init_db.py` | 新增数据库初始化脚本 |

### 删除文件

| 文件 | 说明 |
|------|------|
| `app/core/wework.py` | 企业微信服务类（已删除） |
| `WEWORK_AUTH_GUIDE.md` | 企业微信接入指南（已删除） |
| `WEWORK_INTEGRATION_SUMMARY.md` | 企业微信集成总结（已删除） |

### 文档更新

| 文件 | 变更说明 |
|------|----------|
| `API_DOCUMENTATION.md` | 更新认证接口文档 |
| `API_QUICK_REFERENCE.md` | 更新快速参考手册 |
| `.env.example` | 删除企业微信配置项 |

---

## ⚠️ 注意事项

### 1. 密码安全

- 密码使用 bcrypt 加密存储
- 最小长度：6 字符
- 建议使用强密码

### 2. 生产环境部署

**必须修改默认密码**：
```python
# 修改管理员密码
from app.core.security import get_password_hash
from app.models.user import User

# 在数据库中更新
admin = db.query(User).filter(User.username == "admin").first()
admin.password_hash = get_password_hash("your-strong-password")
db.commit()
```

### 3. 用户注册

当前版本**不提供用户注册接口**，所有用户需要由管理员创建。

如需添加用户，可以：
1. 直接在数据库中插入
2. 编写管理员接口创建用户
3. 运行自定义脚本批量创建

---

## 🔄 迁移指南（如果有旧数据）

如果你有使用企业微信登录的旧数据，需要进行数据迁移：

### 方案1：重新初始化（推荐）

```bash
# 备份旧数据（如果需要）
cp forest_hole.db forest_hole.db.backup

# 删除旧数据库
rm forest_hole.db

# 重新初始化
python init_db.py
```

### 方案2：手动迁移

```python
# 为现有用户添加用户名和密码
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

# 获取所有用户
users = db.query(User).all()

for i, user in enumerate(users):
    # 设置用户名（基于 ID 或其他逻辑）
    user.username = f"user{user.id}"
    # 设置默认密码
    user.password_hash = get_password_hash("changeme123")

db.commit()
db.close()

print("迁移完成！所有用户的默认密码为: changeme123")
```

---

## 📞 技术支持

如有问题，请参考：

1. **API 文档**: `API_DOCUMENTATION.md`
2. **快速参考**: `API_QUICK_REFERENCE.md`
3. **初始化脚本**: `init_db.py`

---

## 📊 接口对比

### 变更前（企业微信登录）

```bash
# 1. 获取授权URL
GET /api/v1/auth/wework/auth-url

# 2. 用户授权后使用 code 登录
POST /api/v1/auth/wework/login
{
  "code": "AUTHORIZATION_CODE"
}
```

### 变更后（用户名密码登录）

```bash
# 直接登录
POST /api/v1/auth/login
{
  "username": "testuser",
  "password": "password123"
}
```

---

**变更完成时间**: 2025-11-30  
**接口总数**: 21 个（保持不变）  
**认证方式**: 用户名密码 + JWT Token
