# 校园树洞 API 接口文档

## 📋 目录

- [基本信息](#基本信息)
- [认证说明](#认证说明)
- [接口列表](#接口列表)
  - [1. 认证接口](#1-认证接口)
  - [2. 帖子接口](#2-帖子接口)
  - [3. 评论接口](#3-评论接口)
  - [4. 表态接口](#4-表态接口)
  - [5. 举报接口](#5-举报接口)
  - [6. 安全检测接口](#6-安全检测接口)
  - [7. 漂流瓶接口](#7-漂流瓶接口)
  - [8. 时间胶囊接口](#8-时间胶囊接口)
  - [9. 投票接口](#9-投票接口)
  - [10. 工具接口](#10-工具接口)
  - [11. 管理员接口](#11-管理员接口)
- [错误码说明](#错误码说明)
- [数据模型](#数据模型)

---

## 基本信息

- **Base URL**: `http://your-domain.com/api/v1`
- **协议**: HTTP/HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8
- **认证方式**: JWT Bearer Token

### 环境地址

| 环境 | 地址 |
|------|------|
| 开发环境 | `http://localhost:8000/api/v1` |
| 测试环境 | `http://test.example.com/api/v1` |
| 生产环境 | `https://api.example.com/api/v1` |

### 在线文档

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 认证说明

### 获取 Token

通过登录接口获取 JWT Token：

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "device_id": "your-device-id"
}
```

### 使用 Token

在请求头中携带 Token：

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token 有效期

- 默认有效期：7天
- 过期后需要重新登录

---

## 接口列表

### 1. 认证接口

#### 1.1 用户登录

**接口说明**: 使用用户名和密码登录系统

**请求方式**: `POST /auth/login`

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名（3-50字符） |
| password | string | 是 | 密码（6-100字符） |

**请求示例**:

```json
{
  "username": "testuser",
  "password": "password123"
}
```

**响应示例**:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**错误响应**:

```json
{
  "detail": "用户名或密码错误"
}
```

**状态码**: 
- `200 OK` - 登录成功
- `401 Unauthorized` - 用户名或密码错误
- `403 Forbidden` - 账号已被封禁

---

### 2. 帖子接口

#### 2.1 获取帖子列表

**接口说明**: 获取帖子列表，支持分页、排序、筛选和搜索

**请求方式**: `GET /posts`

**请求参数**:

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| page | integer | 否 | 1 | 页码 |
| limit | integer | 否 | 20 | 每页数量 |
| sort | string | 否 | new | 排序方式：`new`(最新) / `hot`(热门) |
| tag | string | 否 | - | 标签筛选 |
| keyword | string | 否 | - | 关键词搜索 |

**请求示例**:

```http
GET /posts?page=1&limit=10&sort=hot&tag=study
```

**响应示例**:

```json
{
  "total": 100,
  "page": 1,
  "limit": 10,
  "posts": [
    {
      "id": 1,
      "content": "这是一条帖子内容",
      "media_urls": ["https://example.com/image.jpg"],
      "tag": "study",
      "anonymous_nickname": "焦虑的高三党",
      "status": "active",
      "likes_count": 10,
      "comments_count": 5,
      "has_sos_content": false,
      "created_at": "2025-11-30T12:00:00"
    }
  ]
}
```

#### 2.2 发布新帖子

**接口说明**: 发布新帖子，自动生成匿名昵称

**请求方式**: `POST /posts`

**请求头**: 需要认证

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| content | string | 是 | 帖子内容（1-2000字符） |
| tag | string | 是 | 标签：`crush`/`rant`/`help`/`confession`/`study`/`life`/`other` |
| media_urls | array | 否 | 图片/音频URL列表 |

**请求示例**:

```json
{
  "content": "今天心情不错，分享一下学习心得",
  "tag": "study",
  "media_urls": ["https://example.com/image.jpg"]
}
```

**响应示例**:

```json
{
  "id": 1,
  "content": "今天心情不错，分享一下学习心得",
  "media_urls": ["https://example.com/image.jpg"],
  "tag": "study",
  "anonymous_nickname": "快乐的学霸",
  "status": "active",
  "likes_count": 0,
  "comments_count": 0,
  "has_sos_content": false,
  "created_at": "2025-11-30T12:00:00"
}
```

**状态码**: `201 Created`

#### 2.3 获取帖子详情

**接口说明**: 获取单个帖子的详细信息，包含评论列表

**请求方式**: `GET /posts/{post_id}`

**请求头**: 需要认证

**路径参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | integer | 帖子ID |

**响应示例**:

```json
{
  "id": 1,
  "content": "帖子内容",
  "media_urls": [],
  "tag": "study",
  "anonymous_nickname": "快乐的学霸",
  "status": "active",
  "likes_count": 10,
  "comments_count": 3,
  "has_sos_content": false,
  "created_at": "2025-11-30T12:00:00",
  "comments": [
    {
      "id": 1,
      "content": "评论内容",
      "anonymous_nickname": "沉默的高一生",
      "is_author": false,
      "parent_id": null,
      "created_at": "2025-11-30T12:05:00"
    }
  ]
}
```

#### 2.4 删除帖子

**接口说明**: 删除自己发布的帖子

**请求方式**: `DELETE /posts/{post_id}`

**请求头**: 需要认证

**路径参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | integer | 帖子ID |

**响应示例**:

```json
{
  "message": "帖子已删除"
}
```

---

### 3. 评论接口

#### 3.1 发表评论

**接口说明**: 对帖子发表评论，支持楼中楼回复

**请求方式**: `POST /posts/{post_id}/comments`

**请求头**: 需要认证

**路径参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | integer | 帖子ID |

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| content | string | 是 | 评论内容（1-500字符） |
| parent_id | integer | 否 | 父评论ID（楼中楼） |

**请求示例**:

```json
{
  "content": "说得对！",
  "parent_id": 1
}
```

**响应示例**:

```json
{
  "id": 2,
  "post_id": 1,
  "content": "说得对！",
  "parent_id": 1,
  "anonymous_nickname": "活泼的文科生",
  "is_author": false,
  "created_at": "2025-11-30T12:10:00"
}
```

**状态码**: `201 Created`

---

### 4. 表态接口

#### 4.1 表态/取消表态

**接口说明**: 对帖子进行表态（点赞、抱抱等），支持 Toggle 机制

**请求方式**: `POST /posts/{post_id}/reactions`

**请求头**: 需要认证

**路径参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| post_id | integer | 帖子ID |

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| type | string | 是 | 表态类型：`like`/`hug`/`popcorn`/`plus1` |

**表态类型说明**:

- `like`: 点赞
- `hug`: 抱抱
- `popcorn`: 吃瓜
- `plus1`: +1

**请求示例**:

```json
{
  "type": "like"
}
```

**响应示例**:

```json
{
  "message": "表态成功",
  "action": "added"
}
```

或

```json
{
  "message": "取消表态",
  "action": "removed"
}
```

---

### 5. 举报接口

#### 5.1 提交举报

**接口说明**: 举报不当内容，超过阈值自动隐藏

**请求方式**: `POST /reports`

**请求头**: 需要认证

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| target_type | string | 是 | 举报对象类型：`post`/`comment` |
| target_id | integer | 是 | 举报对象ID |
| reason | string | 是 | 举报理由：`attack`/`privacy`/`fake`/`spam`/`other` |
| description | string | 否 | 详细描述 |

**举报理由说明**:

- `attack`: 人身攻击
- `privacy`: 侵犯隐私
- `fake`: 虚假信息
- `spam`: 垃圾广告
- `other`: 其他

**请求示例**:

```json
{
  "target_type": "post",
  "target_id": 1,
  "reason": "spam",
  "description": "这是垃圾广告"
}
```

**响应示例**:

```json
{
  "message": "举报已提交",
  "reports_count": 3
}
```

**状态码**: `201 Created`

**说明**: 当举报数达到阈值（默认5次）时，内容会自动隐藏

---

### 6. 安全检测接口

#### 6.1 文本安全检测

**接口说明**: 检测文本中的敏感词和 SOS 关键词

**请求方式**: `POST /safety/check-text`

**请求头**: 需要认证

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| content | string | 是 | 待检测的文本内容 |

**请求示例**:

```json
{
  "content": "我感到很抑郁"
}
```

**响应示例**:

```json
{
  "pass_check": false,
  "blocked_words": ["抑郁"],
  "has_sos_content": true,
  "message": "内容包含敏感词"
}
```

---

### 7. 漂流瓶接口

#### 7.1 扔漂流瓶

**接口说明**: 投放一个漂流瓶

**请求方式**: `POST /bottles`

**请求头**: 需要认证

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| content | string | 是 | 漂流瓶内容 |

**请求示例**:

```json
{
  "content": "希望有人能看到这条消息"
}
```

**响应示例**:

```json
{
  "id": 1,
  "content": "希望有人能看到这条消息",
  "created_at": "2025-11-30T12:00:00"
}
```

**状态码**: `201 Created`

#### 7.2 捡漂流瓶

**接口说明**: 随机捡一个漂流瓶（不会捡到自己的）

**请求方式**: `GET /bottles/draw`

**请求头**: 需要认证

**响应示例**:

```json
{
  "id": 2,
  "content": "来自陌生人的消息",
  "created_at": "2025-11-29T10:00:00"
}
```

**错误响应**:

```json
{
  "detail": "暂时没有可捡的漂流瓶"
}
```

**状态码**: `404 Not Found`（没有可用的瓶子）

---

### 8. 时间胶囊接口

#### 8.1 创建时间胶囊

**接口说明**: 创建一个时间胶囊，到期后才能查看

**请求方式**: `POST /time-capsules`

**请求头**: 需要认证

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| content | string | 是 | 胶囊内容 |
| deliver_at | string | 是 | 投递时间（ISO 8601格式） |

**请求示例**:

```json
{
  "content": "给未来的自己：希望你已经考上理想的大学",
  "deliver_at": "2026-06-07T00:00:00"
}
```

**响应示例**:

```json
{
  "id": 1,
  "content": "给未来的自己：希望你已经考上理想的大学",
  "deliver_at": "2026-06-07T00:00:00",
  "is_delivered": false,
  "created_at": "2025-11-30T12:00:00"
}
```

**状态码**: `201 Created`

#### 8.2 获取我的时间胶囊

**接口说明**: 获取已到期的时间胶囊列表

**请求方式**: `GET /time-capsules/my`

**请求头**: 需要认证

**响应示例**:

```json
[
  {
    "id": 1,
    "content": "给未来的自己：希望你已经考上理想的大学",
    "deliver_at": "2025-06-07T00:00:00",
    "is_delivered": true,
    "created_at": "2024-11-30T12:00:00"
  }
]
```

---

### 9. 投票接口

#### 9.1 创建投票

**接口说明**: 创建一个投票

**请求方式**: `POST /polls`

**请求头**: 需要认证

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| title | string | 是 | 投票标题 |
| options | array | 是 | 选项列表（2-10个） |
| expires_at | string | 是 | 过期时间（ISO 8601格式） |

**请求示例**:

```json
{
  "title": "你最喜欢哪个学科？",
  "options": ["数学", "语文", "英语", "物理"],
  "expires_at": "2025-12-31T23:59:59"
}
```

**响应示例**:

```json
{
  "id": 1,
  "title": "你最喜欢哪个学科？",
  "options": ["数学", "语文", "英语", "物理"],
  "created_at": "2025-11-30T12:00:00",
  "expires_at": "2025-12-31T23:59:59"
}
```

**状态码**: `201 Created`

#### 9.2 参与投票

**接口说明**: 对投票进行投票

**请求方式**: `POST /polls/{poll_id}/vote`

**请求头**: 需要认证

**路径参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| poll_id | integer | 投票ID |

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| option_index | integer | 是 | 选项索引（从0开始） |

**请求示例**:

```json
{
  "option_index": 0
}
```

**响应示例**:

```json
{
  "message": "投票成功"
}
```

#### 9.3 获取投票结果

**接口说明**: 获取投票的结果统计

**请求方式**: `GET /polls/{poll_id}`

**请求头**: 需要认证

**路径参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| poll_id | integer | 投票ID |

**响应示例**:

```json
{
  "id": 1,
  "title": "你最喜欢哪个学科？",
  "options": ["数学", "语文", "英语", "物理"],
  "created_at": "2025-11-30T12:00:00",
  "expires_at": "2025-12-31T23:59:59",
  "votes": [15, 8, 12, 10],
  "total_votes": 45
}
```

---

### 10. 工具接口

#### 10.1 获取每日信息

**接口说明**: 获取高考倒计时和每日话题

**请求方式**: `GET /utility/daily-info`

**请求头**: 需要认证

**响应示例**:

```json
{
  "countdown": {
    "event": "高考",
    "days": 188,
    "date": "2026-06-07"
  },
  "daily_topic": {
    "title": "今天遇到的温暖瞬间",
    "id": 1
  }
}
```

---

### 11. 管理员接口

#### 11.1 获取仪表盘数据

**接口说明**: 获取管理后台的统计数据

**请求方式**: `GET /admin/dashboard`

**请求头**: 需要管理员认证

**响应示例**:

```json
{
  "daily_active_users": 150,
  "daily_posts": 45,
  "pending_audits": 3,
  "total_users": 1200,
  "total_posts": 5600
}
```

#### 11.2 获取待审核列表

**接口说明**: 获取需要审核的内容列表

**请求方式**: `GET /admin/audit/list`

**请求头**: 需要管理员认证

**请求参数**:

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| status_filter | string | 否 | pending | 状态筛选：`pending`/`hidden`/`all` |

**响应示例**:

```json
[
  {
    "id": 1,
    "content": "待审核的内容",
    "status": "pending",
    "reports_count": 3,
    "created_at": "2025-11-30T12:00:00"
  }
]
```

#### 11.3 执行审核操作

**接口说明**: 对内容进行审核操作

**请求方式**: `PUT /admin/audit/{target_id}`

**请求头**: 需要管理员认证

**路径参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| target_id | integer | 目标内容ID |

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| target_type | string | 是 | 内容类型：`post`/`comment` |
| action | string | 是 | 操作：`approve`/`reject`/`ban_user` |

**操作说明**:

- `approve`: 通过审核
- `reject`: 拒绝（删除内容）
- `ban_user`: 封禁用户并删除内容

**请求示例**:

```json
{
  "target_type": "post",
  "action": "approve"
}
```

**响应示例**:

```json
{
  "message": "审核通过",
  "action": "approve"
}
```

#### 11.4 获取举报列表

**接口说明**: 获取所有举报记录的统计

**请求方式**: `GET /admin/reports`

**请求头**: 需要管理员认证

**响应示例**:

```json
{
  "total": 15,
  "stats": [
    {
      "target_type": "post",
      "target_id": 1,
      "count": 5,
      "reasons": ["spam", "spam", "attack", "spam", "other"]
    }
  ]
}
```

---

## 错误码说明

### HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或 Token 无效 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 422 | 请求参数验证失败 |
| 500 | 服务器内部错误 |

### 错误响应格式

```json
{
  "detail": "错误信息描述"
}
```

或

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "content"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

---

## 数据模型

### 帖子状态

| 值 | 说明 |
|----|------|
| pending | 待审核 |
| active | 正常显示 |
| hidden | 已隐藏（被举报） |
| deleted | 已删除 |

### 标签类型

| 值 | 说明 |
|----|------|
| crush | 暗恋墙 |
| rant | 吐槽 |
| help | 求助 |
| confession | 表白 |
| study | 学习 |
| life | 生活 |
| other | 其他 |

### 表态类型

| 值 | 说明 | 图标建议 |
|----|------|----------|
| like | 点赞 | 👍 |
| hug | 抱抱 | 🤗 |
| popcorn | 吃瓜 | 🍿 |
| plus1 | +1 | ➕ |

### 举报理由

| 值 | 说明 |
|----|------|
| attack | 人身攻击 |
| privacy | 侵犯隐私 |
| fake | 虚假信息 |
| spam | 垃圾广告 |
| other | 其他 |

---

## 使用示例

### JavaScript (Fetch API)

```javascript
// 登录
const login = async () => {
  const response = await fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      device_id: 'my-device-id'
    })
  });
  const data = await response.json();
  return data.access_token;
};

// 获取帖子列表
const getPosts = async (token) => {
  const response = await fetch('http://localhost:8000/api/v1/posts?sort=hot&page=1&limit=10', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return await response.json();
};

// 发布帖子
const createPost = async (token, content, tag) => {
  const response = await fetch('http://localhost:8000/api/v1/posts', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      content,
      tag
    })
  });
  return await response.json();
};
```

### Python (Requests)

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 登录
def login(device_id):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"device_id": device_id}
    )
    return response.json()["access_token"]

# 获取帖子列表
def get_posts(token, sort="hot", page=1, limit=10):
    response = requests.get(
        f"{BASE_URL}/posts",
        headers={"Authorization": f"Bearer {token}"},
        params={"sort": sort, "page": page, "limit": limit}
    )
    return response.json()

# 发布帖子
def create_post(token, content, tag):
    response = requests.post(
        f"{BASE_URL}/posts",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": content, "tag": tag}
    )
    return response.json()
```

### cURL

```bash
# 登录
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"device_id": "test-device"}'

# 获取帖子列表
curl -X GET "http://localhost:8000/api/v1/posts?sort=hot&page=1&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 发布帖子
curl -X POST "http://localhost:8000/api/v1/posts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "测试帖子", "tag": "test"}'
```

---

## 最佳实践

### 1. Token 管理

- 将 Token 存储在本地（localStorage/sessionStorage）
- 每次请求自动携带 Token
- Token 过期时自动重新登录

### 2. 错误处理

```javascript
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || '请求失败');
  }
  return await response.json();
};
```

### 3. 请求封装

```javascript
class TreeholeAPI {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.token = null;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    return await this.handleResponse(response);
  }

  async handleResponse(response) {
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || '请求失败');
    }
    return await response.json();
  }

  async login(deviceId) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ device_id: deviceId }),
    });
    this.token = data.access_token;
    return data;
  }

  async getPosts(params = {}) {
    const query = new URLSearchParams(params).toString();
    return await this.request(`/posts?${query}`);
  }

  async createPost(content, tag, mediaUrls = []) {
    return await this.request('/posts', {
      method: 'POST',
      body: JSON.stringify({ content, tag, media_urls: mediaUrls }),
    });
  }
}

// 使用
const api = new TreeholeAPI('http://localhost:8000/api/v1');
await api.login('my-device-id');
const posts = await api.getPosts({ sort: 'hot', page: 1 });
```

---

## 更新日志

### v1.0.0 (2025-11-30)

- ✨ 初始版本发布
- ✅ 实现 21 个核心 API 接口
- ✅ 完整的认证和权限系统
- ✅ 内容安全检测功能
- ✅ 管理后台接口

---

## 联系我们

- **技术支持**: support@example.com
- **问题反馈**: https://github.com/your-repo/issues
- **API 文档**: http://localhost:8000/docs

---

**最后更新**: 2025-11-30
**文档版本**: v1.0.0
