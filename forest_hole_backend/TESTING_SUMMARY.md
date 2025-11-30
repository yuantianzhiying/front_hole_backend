# 测试工具总结

## 📦 已创建的测试工具

我为你创建了三个完整的测试程序：

### 1️⃣ test_import.py - 模块导入测试
- **用途**: 验证所有 Python 模块是否正确安装和导入
- **运行**: `python test_import.py`
- **耗时**: ~1秒
- **适用**: 安装依赖后的第一次验证

### 2️⃣ quick_test.py - 快速接口测试
- **用途**: 快速验证核心 API 接口是否可用
- **运行**: `python quick_test.py`
- **耗时**: ~5-10秒
- **适用**: 日常开发时的快速验证
- **测试内容**:
  - ✓ 健康检查
  - ✓ 用户认证
  - ✓ 帖子 CRUD
  - ✓ 安全检测
  - ✓ 工具接口
  - ✓ 管理员接口

### 3️⃣ test_api.py - 完整接口测试
- **用途**: 全面测试所有 21+ 个 API 接口
- **运行**: `python test_api.py`
- **耗时**: ~30-60秒
- **适用**: 发布前的完整功能测试
- **特点**:
  - 🎨 彩色终端输出
  - 📊 详细的测试报告
  - 🔗 自动处理接口依赖关系
  - 💾 自动保存测试数据
  - 🧹 自动清理测试数据

## 🚀 快速开始

### 步骤 1: 启动服务

```bash
cd forest_hole_backend
uv run uvicorn main:app --reload
```

### 步骤 2: 运行测试（新终端）

```bash
# 推荐：先运行快速测试
python quick_test.py

# 然后运行完整测试
python test_api.py
```

## 📋 测试覆盖范围

### 认证模块 (1个接口)
- ✅ POST /auth/login - 用户登录/注册

### 帖子模块 (4个接口)
- ✅ GET /posts - 获取帖子列表（支持排序、筛选、搜索）
- ✅ POST /posts - 发布新帖子
- ✅ GET /posts/{id} - 获取帖子详情
- ✅ DELETE /posts/{id} - 删除帖子

### 评论模块 (1个接口)
- ✅ POST /posts/{id}/comments - 发表评论（支持楼中楼）

### 表态模块 (1个接口)
- ✅ POST /posts/{id}/reactions - 表态/点赞（Toggle机制）

### 举报模块 (1个接口)
- ✅ POST /reports - 提交举报

### 安全模块 (1个接口)
- ✅ POST /safety/check-text - 文本安全检测

### 漂流瓶模块 (2个接口)
- ✅ POST /bottles - 扔漂流瓶
- ✅ GET /bottles/draw - 捡漂流瓶

### 时间胶囊模块 (2个接口)
- ✅ POST /time-capsules - 创建时间胶囊
- ✅ GET /time-capsules/my - 获取我的时间胶囊

### 投票模块 (3个接口)
- ✅ POST /polls - 创建投票
- ✅ GET /polls/{id} - 获取投票结果
- ✅ POST /polls/{id}/vote - 参与投票

### 工具模块 (1个接口)
- ✅ GET /utility/daily-info - 获取每日信息

### 管理员模块 (4个接口)
- ✅ GET /admin/dashboard - 获取仪表盘数据
- ✅ GET /admin/audit/list - 获取待审核列表
- ✅ PUT /admin/audit/{id} - 执行审核操作
- ✅ GET /admin/reports - 获取举报列表

**总计**: 21 个 API 接口 ✅

## 📊 测试输出示例

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

详细测试请运行: python test_api.py
API文档: http://127.0.0.1:8000/docs
```

### 完整测试输出（部分）

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

============================================================
  2. 帖子接口 (Posts)
============================================================

ℹ 测试: 发布新帖子
      POST /posts
✓ 状态码: 200
      响应: {
  "id": 1,
  "content": "这是一个测试帖子，测试敏感词过滤功能",
  "tag": "test",
  "anonymous_nickname": "焦虑的高三党",
  ...
}...

... (更多测试输出)

============================================================
  测试总结
============================================================

测试数据:
  token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  post_id: 1
  comment_id: 1
  bottle_id: 1
  poll_id: 1

✅ 所有接口测试完成！

访问 API 文档查看更多信息:
  http://127.0.0.1:8000/docs
```

## 🔧 测试功能特点

### test_api.py 的高级特性

1. **彩色输出**
   - 🟢 绿色 = 成功
   - 🔴 红色 = 失败
   - 🔵 蓝色 = 信息
   - 🟡 黄色 = 警告

2. **智能依赖处理**
   - 自动保存登录 Token
   - 自动保存创建的资源 ID
   - 按依赖顺序执行测试

3. **详细日志**
   - 显示请求方法和路径
   - 显示响应状态码
   - 显示响应内容（前200字符）

4. **错误处理**
   - 连接失败提示
   - 认证失败提示
   - 跳过依赖缺失的测试

5. **自动清理**
   - 测试结束后删除测试数据
   - 避免污染数据库

## 🛠️ 自定义测试

### 修改测试配置

编辑 `test_api.py`:

```python
# 修改服务地址
BASE_URL = "http://your-server.com/api/v1"

# 修改管理员 Token
ADMIN_TOKEN = "your-admin-token"
```

### 添加自定义测试

```python
def test_your_feature():
    """测试你的新功能"""
    print_section("X. 你的功能")
    
    headers = get_auth_headers()
    
    test_request(
        "POST",
        "/your-endpoint",
        "测试描述",
        data={"key": "value"},
        headers=headers
    )

# 在 main() 函数中调用
test_your_feature()
```

## 📚 相关文档

- **TEST_GUIDE.md** - 完整的测试指南
- **RUN_TESTS.md** - 快速运行指南
- **API_EXAMPLES.md** - API 使用示例
- **README.md** - 项目主文档

## 🎯 使用建议

### 开发阶段
1. 修改代码后运行 `quick_test.py` 快速验证
2. 每天结束前运行 `test_api.py` 全面检查

### 发布前
1. 运行 `test_api.py` 确保所有功能正常
2. 检查测试输出，确保没有错误
3. 访问 API 文档手动测试关键流程

### 生产环境
1. 部署后立即运行 `quick_test.py`
2. 定期运行 `test_api.py` 监控服务状态
3. 集成到 CI/CD 流程中自动测试

## ❓ 常见问题

### Q: 测试失败怎么办？

1. **检查服务是否启动**
   ```bash
   curl http://127.0.0.1:8000/health
   ```

2. **检查依赖是否安装**
   ```bash
   python test_import.py
   ```

3. **查看服务日志**
   - 检查终端中的错误信息
   - 查看是否有异常堆栈

### Q: 某些接口返回 404 正常吗？

是的，以下情况是正常的：
- 捡漂流瓶时没有可用的瓶子
- 查询不存在的资源
- 时间胶囊未到投递时间

### Q: 如何测试生产环境？

修改 `test_api.py` 中的 `BASE_URL`:

```python
BASE_URL = "https://your-production-api.com/api/v1"
```

**注意**: 生产环境测试会创建真实数据，请谨慎使用！

## 🎉 总结

你现在拥有：
- ✅ 3 个完整的测试程序
- ✅ 覆盖所有 21 个 API 接口
- ✅ 详细的测试文档
- ✅ 彩色的终端输出
- ✅ 智能的错误处理

开始测试吧！🚀

```bash
# 启动服务
uv run uvicorn main:app --reload

# 运行测试（新终端）
python quick_test.py
python test_api.py
```

祝测试顺利！如有问题，请查看 `TEST_GUIDE.md` 获取更多帮助。
