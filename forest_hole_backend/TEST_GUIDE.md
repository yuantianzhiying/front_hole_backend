# API 测试指南

## 测试脚本说明

本项目提供了三个测试工具：

### 1. 模块导入测试 (`test_import.py`)

测试所有 Python 模块是否可以正常导入。

```bash
python test_import.py
```

**用途**: 在安装依赖后，验证项目结构是否正确。

---

### 2. 快速接口测试 (`quick_test.py`)

快速测试主要 API 接口是否可用。

```bash
python quick_test.py
```

**特点**:
- 测试速度快（约 5-10 秒）
- 覆盖核心接口
- 输出简洁清晰
- 适合日常开发验证

**测试内容**:
- ✓ 健康检查
- ✓ 用户认证
- ✓ 帖子创建和查询
- ✓ 安全检测
- ✓ 工具接口
- ✓ 管理员接口

---

### 3. 完整接口测试 (`test_api.py`)

全面测试所有 API 接口的功能。

```bash
python test_api.py
```

**特点**:
- 测试全面（21+ 个接口）
- 详细的输出信息
- 彩色终端显示
- 自动保存测试数据
- 测试接口之间的关联

**测试内容**:
- ✓ 健康检查
- ✓ 认证接口（登录/注册）
- ✓ 帖子接口（创建、列表、详情、删除）
- ✓ 评论接口（发表评论、楼中楼）
- ✓ 表态接口（点赞、抱抱、Toggle）
- ✓ 举报接口
- ✓ 安全检测接口
- ✓ 漂流瓶接口（扔瓶子、捡瓶子）
- ✓ 时间胶囊接口
- ✓ 投票接口（创建、投票、查看结果）
- ✓ 工具接口（每日信息）
- ✓ 管理员接口（仪表盘、审核、举报）

---

## 使用步骤

### 第一步：启动服务

```bash
# 在 forest_hole_backend 目录下
uv run uvicorn main:app --reload
```

或者

```bash
python run.py
```

等待服务启动，看到以下信息表示成功：

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxx] using WatchFiles
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 第二步：运行测试

**新终端窗口**中运行测试脚本：

```bash
# 快速测试（推荐先运行）
python quick_test.py

# 完整测试
python test_api.py
```

---

## 测试输出示例

### 快速测试输出

```
============================================================
  快速接口测试
============================================================

[健康检查]
✓ Health Check: 200

[基础接口]
✓ Root: 200
✓ API Docs: 200

[认证接口]
✓ Login/Register: 200
  Token: eyJhbGciOiJIUzI1NiIsInR5cCI6...

[帖子接口]
✓ Get Posts: 200
✓ Create Post: 200
  Post ID: 1
✓ Get Post Detail: 200

[其他接口]
✓ Safety Check: 200
✓ Daily Info: 200
✓ Draw Bottle: 404

[管理员接口]
✓ Admin Dashboard: 200

============================================================
✅ 快速测试完成！
============================================================
```

### 完整测试输出

```
============================================================
  校园树洞 API 接口测试程序
============================================================

ℹ 测试目标: http://127.0.0.1:8000/api/v1
ℹ 开始测试...

============================================================
  0. 健康检查
============================================================

✓ 服务运行正常

============================================================
  1. 认证接口 (Authentication)
============================================================

ℹ 测试: 用户登录/注册
      POST /auth/login
✓ 状态码: 200
      响应: {
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1
}...
ℹ 已保存 token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
✓ 登录成功，Token: eyJhbGciOiJIUzI1NiIsI...

... (更多测试输出)

============================================================
  测试总结
============================================================

测试数据:
  token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  post_id: 1
  comment_id: 1
  poll_id: 1

✅ 所有接口测试完成！

访问 API 文档查看更多信息:
  http://127.0.0.1:8000/docs
```

---

## 常见问题

### Q: 提示"连接失败"

**原因**: 服务未启动或端口不正确。

**解决**:
1. 确保服务已启动: `uvicorn main:app --reload`
2. 检查端口是否为 8000
3. 查看服务是否有错误日志

### Q: 提示"认证失败"

**原因**: Token 过期或无效。

**解决**:
1. 重新运行测试脚本（会自动重新登录）
2. 检查 `SECRET_KEY` 配置是否正确

### Q: 某些接口返回 404

**原因**: 
- 接口路径不存在
- 数据不存在（如捡漂流瓶时没有可用的瓶子）

**解决**: 这是正常的，某些接口在数据为空时会返回 404。

### Q: 管理员接口测试失败

**原因**: `ADMIN_TOKEN` 不正确。

**解决**:
1. 检查 `.env` 文件中的 `ADMIN_TOKEN`
2. 修改 `test_api.py` 中的 `ADMIN_TOKEN` 变量

---

## 自定义测试

你可以修改测试脚本来测试特定场景：

### 修改测试数据

编辑 `test_api.py` 中的测试数据：

```python
# 修改帖子内容
data={
    "content": "你的自定义内容",
    "tag": "your_tag",
    "media_urls": ["https://your-image-url.jpg"]
}
```

### 添加新的测试用例

```python
def test_your_feature():
    """测试你的新功能"""
    print_section("X. 你的功能测试")
    
    headers = get_auth_headers()
    
    test_request(
        "POST",
        "/your-endpoint",
        "测试描述",
        data={"key": "value"},
        headers=headers
    )
```

### 修改测试配置

```python
# 修改 BASE_URL
BASE_URL = "http://your-server.com/api/v1"

# 修改 ADMIN_TOKEN
ADMIN_TOKEN = "your-admin-token"
```

---

## 使用 Postman 测试

如果你更喜欢使用 Postman：

1. 访问 http://127.0.0.1:8000/openapi.json
2. 在 Postman 中导入 OpenAPI 规范
3. 创建环境变量：
   - `base_url`: `http://127.0.0.1:8000/api/v1`
   - `token`: 登录后获取的 JWT
   - `admin_token`: 管理员 Token

---

## 使用 curl 测试

参考 `API_EXAMPLES.md` 文件中的 curl 示例。

示例：

```bash
# 登录
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"device_id": "test-device"}'

# 获取帖子列表
curl -X GET "http://127.0.0.1:8000/api/v1/posts?sort=new&page=1&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 性能测试

如果需要进行压力测试，可以使用以下工具：

### 使用 Apache Bench (ab)

```bash
# 测试健康检查接口
ab -n 1000 -c 10 http://127.0.0.1:8000/health
```

### 使用 wrk

```bash
# 测试帖子列表接口
wrk -t4 -c100 -d30s http://127.0.0.1:8000/api/v1/posts
```

### 使用 locust

创建 `locustfile.py`:

```python
from locust import HttpUser, task, between

class TreeholeUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # 登录获取 token
        response = self.client.post("/api/v1/auth/login", 
                                    json={"device_id": "load-test"})
        self.token = response.json()["access_token"]
    
    @task
    def get_posts(self):
        self.client.get("/api/v1/posts", 
                       headers={"Authorization": f"Bearer {self.token}"})
```

运行：

```bash
locust -f locustfile.py
```

---

## 持续集成 (CI)

可以将测试脚本集成到 CI/CD 流程中：

### GitHub Actions 示例

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Start server
      run: |
        uvicorn main:app &
        sleep 5
    
    - name: Run tests
      run: |
        python test_api.py
```

---

## 总结

- 🚀 **快速验证**: 使用 `quick_test.py`
- 🔍 **全面测试**: 使用 `test_api.py`
- 📖 **API 文档**: http://127.0.0.1:8000/docs
- 🛠️ **自定义测试**: 修改测试脚本或使用 Postman

祝测试顺利！🎉
