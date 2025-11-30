# 校园树洞后端 API

基于 FastAPI 构建的校园匿名树洞社区后端系统。

## 功能特性

### 核心功能
- ✅ **匿名发布** - 自动生成随机昵称，保护用户隐私
- ✅ **浏览筛选** - 支持时间流/热度榜/标签筛选/关键词搜索
- ✅ **评论互动** - 支持评论和楼中楼回复，自动标识楼主
- ✅ **轻量表态** - 点赞、抱抱、吃瓜、+1 等多种表态方式

### 安全与风控
- ✅ **敏感词过滤** - 自动检测和过滤敏感内容
- ✅ **SOS检测** - 识别自杀/抑郁等关键词，触发心理援助提示
- ✅ **举报机制** - 用户举报，超过阈值自动隐藏
- ✅ **内容审核** - 管理后台支持人工审核

### 趣味功能
- ✅ **漂流瓶** - 扔瓶子/捡瓶子，随机匹配陌生人的秘密
- ✅ **时间胶囊** - 给未来的自己留言
- ✅ **投票功能** - 创建和参与投票
- ✅ **实用工具** - 高考倒计时、每日话题

### 管理后台
- ✅ **数据仪表盘** - 日活、发帖量、待审核数等统计
- ✅ **内容审核** - 通过/拒绝/封禁操作
- ✅ **举报管理** - 查看举报列表和统计

## 技术栈

- **框架**: FastAPI 0.104+
- **数据库**: SQLAlchemy (支持 SQLite/MySQL/PostgreSQL)
- **认证**: JWT (JSON Web Tokens)
- **密码加密**: Passlib + Bcrypt

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

**重要配置项**：
- `SECRET_KEY`: JWT密钥，生产环境必须修改
- `ADMIN_TOKEN`: 管理员令牌，生产环境必须修改
- `DATABASE_URL`: 数据库连接字符串

### 3. 运行服务

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务将在 `http://localhost:8000` 启动。

### 4. 访问文档

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API 文档

### 基础 URL

```
http://localhost:8000/api/v1
```

### 认证

所有需要认证的接口都需要在 Header 中携带 JWT Token：

```
Authorization: Bearer <your_token>
```

### 主要接口

#### 1. 认证
- `POST /auth/login` - 登录/注册

#### 2. 帖子
- `GET /posts` - 获取帖子列表
- `POST /posts` - 发布帖子
- `GET /posts/{id}` - 获取帖子详情
- `DELETE /posts/{id}` - 删除帖子

#### 3. 评论
- `POST /posts/{id}/comments` - 发表评论

#### 4. 表态
- `POST /posts/{id}/reactions` - 点赞/表态

#### 5. 举报
- `POST /reports` - 提交举报

#### 6. 安全检测
- `POST /safety/check-text` - 文本安全检测

#### 7. 漂流瓶
- `POST /bottles` - 扔漂流瓶
- `GET /bottles/draw` - 捡漂流瓶

#### 8. 时间胶囊
- `POST /time-capsules` - 创建时间胶囊
- `GET /time-capsules/my` - 获取我的时间胶囊

#### 9. 投票
- `POST /polls` - 创建投票
- `GET /polls/{id}` - 获取投票结果
- `POST /polls/{id}/vote` - 参与投票

#### 10. 实用工具
- `GET /utility/daily-info` - 获取每日信息

#### 11. 管理后台（需要管理员权限）
- `GET /admin/dashboard` - 仪表盘数据
- `GET /admin/audit/list` - 待审核列表
- `PUT /admin/audit/{id}` - 执行审核操作
- `GET /admin/reports` - 举报列表

## 项目结构

```
forest_hole_backend/
├── main.py                 # 应用入口
├── requirements.txt        # 依赖列表
├── .env.example           # 环境变量示例
├── README.md              # 项目文档
└── app/
    ├── __init__.py
    ├── api/               # API路由
    │   └── v1/
    │       ├── __init__.py
    │       ├── auth.py
    │       ├── posts.py
    │       ├── comments.py
    │       ├── reactions.py
    │       ├── reports.py
    │       ├── safety.py
    │       ├── bottles.py
    │       ├── time_capsules.py
    │       ├── polls.py
    │       ├── utility.py
    │       └── admin.py
    ├── core/              # 核心功能
    │   ├── __init__.py
    │   ├── config.py      # 配置
    │   ├── database.py    # 数据库连接
    │   ├── security.py    # 安全认证
    │   └── utils.py       # 工具函数
    ├── models/            # 数据库模型
    │   ├── __init__.py
    │   ├── user.py
    │   ├── post.py
    │   ├── comment.py
    │   ├── reaction.py
    │   ├── report.py
    │   ├── bottle.py
    │   ├── time_capsule.py
    │   └── poll.py
    └── schemas/           # Pydantic模型
        ├── __init__.py
        ├── user.py
        ├── post.py
        ├── comment.py
        ├── reaction.py
        ├── report.py
        ├── bottle.py
        ├── time_capsule.py
        ├── poll.py
        ├── admin.py
        └── safety.py
```

## 数据库设计

### 核心表
- `users` - 用户表（存储真实身份）
- `posts` - 帖子表
- `comments` - 评论表
- `reactions` - 表态表
- `reports` - 举报表

### 功能表
- `bottles` - 漂流瓶表
- `time_capsules` - 时间胶囊表
- `polls` - 投票表
- `poll_votes` - 投票记录表

## 安全特性

### 1. 匿名机制
- 数据库存储真实用户ID（用于追溯和封禁）
- API返回时只显示随机生成的匿名昵称
- 前端完全无法获取真实用户信息

### 2. 敏感词过滤
- 自动检测和替换敏感词
- 可在 `config.py` 中配置敏感词列表

### 3. SOS检测
- 识别自杀、抑郁等关键词
- 返回特殊标记，前端可弹出心理援助信息

### 4. 举报机制
- 用户可举报不当内容
- 超过阈值（默认5次）自动隐藏
- 管理员可人工审核

### 5. 封禁机制
- 管理员可封禁违规用户
- 被封禁用户无法登录和发布内容

## 部署建议

### 生产环境配置

1. **修改密钥**
   ```bash
   # 生成随机密钥
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **使用生产级数据库**
   - 推荐使用 PostgreSQL 或 MySQL
   - 不要在生产环境使用 SQLite

3. **配置 CORS**
   - 在 `.env` 中设置允许的前端域名
   - 不要使用 `*` 允许所有域名

4. **使用 HTTPS**
   - 配置 SSL 证书
   - 使用 Nginx 作为反向代理

5. **图片存储**
   - 使用云存储服务（阿里云OSS、七牛云等）
   - 不要将图片存储在数据库中

### 推荐部署方案

```bash
# 使用 Gunicorn + Uvicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 开发指南

### 添加新功能

1. 在 `models/` 中创建数据库模型
2. 在 `schemas/` 中创建 Pydantic 模型
3. 在 `api/v1/` 中创建路由
4. 在 `api/v1/__init__.py` 中注册路由

### 运行测试

```bash
# TODO: 添加测试用例
pytest
```

## 常见问题

### Q: 如何修改敏感词列表？
A: 编辑 `app/core/config.py` 中的 `SENSITIVE_WORDS` 列表。

### Q: 如何添加管理员？
A: 直接在数据库中将用户的 `is_admin` 字段设置为 `True`。

### Q: 如何备份数据库？
A: 
- SQLite: 直接复制 `.db` 文件
- MySQL/PostgreSQL: 使用相应的备份工具

### Q: 如何集成微信小程序登录？
A: 在 `app/api/v1/auth.py` 中实现微信登录逻辑，调用微信 API 获取 openid。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue 或联系开发者。
