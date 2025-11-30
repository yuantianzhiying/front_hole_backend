# 如何运行测试

## 快速开始

### 1. 启动服务（终端1）

```bash
cd forest_hole_backend
uv run uvicorn main:app --reload
```

等待看到：
```
INFO:     Application startup complete.
```

### 2. 运行测试（终端2）

**快速测试（推荐）：**
```bash
cd forest_hole_backend
python quick_test.py
```

**完整测试：**
```bash
cd forest_hole_backend
python test_api.py
```

## 测试脚本说明

| 脚本 | 用途 | 耗时 | 适用场景 |
|------|------|------|----------|
| `test_import.py` | 测试模块导入 | 1秒 | 安装依赖后验证 |
| `quick_test.py` | 快速接口测试 | 5-10秒 | 日常开发验证 |
| `test_api.py` | 完整接口测试 | 30-60秒 | 全面功能测试 |

## 预期输出

### 成功示例

```
✓ Health Check: 200
✓ Login/Register: 200
✓ Get Posts: 200
✓ Create Post: 200
✅ 快速测试完成！
```

### 失败示例

```
✗ Health Check: 连接失败
❌ 服务未启动！请先运行: uvicorn main:app --reload
```

## 故障排除

### 问题1: 连接失败
- **检查**: 服务是否启动
- **解决**: `uvicorn main:app --reload`

### 问题2: 模块导入错误
- **检查**: 依赖是否安装
- **解决**: `uv sync` 或 `pip install -r requirements.txt`

### 问题3: 认证失败
- **检查**: SECRET_KEY 配置
- **解决**: 检查 `.env` 文件

## 查看详细文档

完整测试指南请查看：`TEST_GUIDE.md`

## API 文档

启动服务后访问：http://127.0.0.1:8000/docs
