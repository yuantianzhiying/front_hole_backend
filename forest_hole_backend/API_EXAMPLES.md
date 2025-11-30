# API 使用示例

## 1. 用户登录/注册

### 请求
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test-device-123"
  }'
```

### 响应
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## 2. 发布帖子

### 请求
```bash
curl -X POST "http://localhost:8000/api/v1/posts" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "今天心情不错，分享一下",
    "tag": "life",
    "media_urls": []
  }'
```

### 响应
```json
{
  "id": 1,
  "content": "今天心情不错，分享一下",
  "media_urls": [],
  "tag": "life",
  "anonymous_nickname": "快乐的高三党",
  "status": "active",
  "likes_count": 0,
  "comments_count": 0,
  "has_sos_content": false,
  "created_at": "2024-01-01T12:00:00Z"
}
```

## 3. 获取帖子列表

### 最新帖子
```bash
curl "http://localhost:8000/api/v1/posts?page=1&limit=20&sort=new"
```

### 热门帖子
```bash
curl "http://localhost:8000/api/v1/posts?page=1&limit=20&sort=hot"
```

### 按标签筛选
```bash
curl "http://localhost:8000/api/v1/posts?tag=crush"
```

### 关键词搜索
```bash
curl "http://localhost:8000/api/v1/posts?keyword=高考"
```

## 4. 发表评论

### 请求
```bash
curl -X POST "http://localhost:8000/api/v1/posts/1/comments" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "说得对！"
  }'
```

### 楼中楼回复
```bash
curl -X POST "http://localhost:8000/api/v1/posts/1/comments" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "同意楼上",
    "parent_id": 5
  }'
```

## 5. 点赞/表态

### 请求
```bash
curl -X POST "http://localhost:8000/api/v1/posts/1/reactions" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "like"
  }'
```

### 表态类型
- `like`: 点赞
- `hug`: 抱抱
- `popcorn`: 吃瓜
- `plus1`: +1

## 6. 举报内容

### 请求
```bash
curl -X POST "http://localhost:8000/api/v1/reports" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "target_type": "post",
    "target_id": 1,
    "reason": "attack",
    "description": "包含人身攻击"
  }'
```

### 举报理由
- `attack`: 人身攻击
- `privacy`: 侵犯隐私
- `fake`: 虚假信息
- `spam`: 垃圾信息
- `other`: 其他

## 7. 文本安全检测

### 请求
```bash
curl -X POST "http://localhost:8000/api/v1/safety/check-text" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "测试内容"
  }'
```

### 响应
```json
{
  "pass_check": true,
  "blocked_words": [],
  "has_sos_content": false,
  "message": "内容安全"
}
```

## 8. 漂流瓶

### 扔漂流瓶
```bash
curl -X POST "http://localhost:8000/api/v1/bottles" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是我的秘密"
  }'
```

### 捡漂流瓶
```bash
curl "http://localhost:8000/api/v1/bottles/draw" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 9. 时间胶囊

### 创建时间胶囊
```bash
curl -X POST "http://localhost:8000/api/v1/time-capsules" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "给未来的自己",
    "deliver_at": "2025-06-07T00:00:00Z"
  }'
```

### 获取我的时间胶囊
```bash
curl "http://localhost:8000/api/v1/time-capsules/my" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 10. 投票

### 创建投票
```bash
curl -X POST "http://localhost:8000/api/v1/polls" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "你最喜欢的科目？",
    "options": ["数学", "语文", "英语", "物理"]
  }'
```

### 参与投票
```bash
curl -X POST "http://localhost:8000/api/v1/polls/1/vote" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "option_index": 0
  }'
```

### 查看投票结果
```bash
curl "http://localhost:8000/api/v1/polls/1"
```

## 11. 实用工具

### 获取每日信息
```bash
curl "http://localhost:8000/api/v1/utility/daily-info"
```

### 响应
```json
{
  "countdown": {
    "event": "高考",
    "days": 100,
    "date": "2025-06-07"
  },
  "daily_topic": {
    "title": "今天最尴尬的事",
    "id": 1
  }
}
```

## 12. 管理后台（需要管理员权限）

### 获取仪表盘数据
```bash
curl "http://localhost:8000/api/v1/admin/dashboard" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### 获取待审核列表
```bash
curl "http://localhost:8000/api/v1/admin/audit/list?status=pending" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

### 审核操作
```bash
# 通过审核
curl -X PUT "http://localhost:8000/api/v1/admin/audit/1" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "approve",
    "target_type": "post"
  }'

# 拒绝（删除）
curl -X PUT "http://localhost:8000/api/v1/admin/audit/1" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "reject",
    "target_type": "post"
  }'

# 封禁用户
curl -X PUT "http://localhost:8000/api/v1/admin/audit/1" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "ban_user",
    "target_type": "post"
  }'
```

### 查看举报列表
```bash
curl "http://localhost:8000/api/v1/admin/reports" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

## 注意事项

1. **认证**: 除了登录接口，其他接口都需要在 Header 中携带 JWT Token
2. **管理员权限**: 管理后台接口需要使用配置文件中的 `ADMIN_TOKEN`
3. **分页**: 列表接口支持 `page` 和 `limit` 参数
4. **时区**: 所有时间都使用 UTC 时区
5. **错误处理**: API 会返回标准的 HTTP 状态码和错误信息
