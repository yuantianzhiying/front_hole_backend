# 安装指南

## 环境要求

- Python 3.8+
- pip

## 安装步骤

### 1. 安装依赖

```bash
# Windows
python -m pip install -r requirements.txt

# Linux/Mac
pip3 install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`：

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

然后编辑 `.env` 文件，修改以下配置：

```env
SECRET_KEY=your-random-secret-key-here
ADMIN_TOKEN=your-admin-token-here
```

**生成随机密钥：**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. 启动服务

#### 方式一：使用 run.py

```bash
python run.py
```

#### 方式二：使用 uvicorn 命令

```bash
# Windows
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Linux/Mac
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问 API 文档

启动成功后，访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## 常见问题

### Q: 提示找不到 pip 命令

**解决方案：**

```bash
# 使用 python -m pip 代替 pip
python -m pip install -r requirements.txt
```

### Q: 提示缺少某个模块

**解决方案：**

```bash
# 单独安装缺失的模块
python -m pip install fastapi uvicorn sqlalchemy pydantic
```

### Q: 数据库连接失败

**解决方案：**

- 默认使用 SQLite，不需要额外配置
- 数据库文件会自动创建在项目根目录：`treehole.db`
- 如果使用 MySQL/PostgreSQL，需要修改 `.env` 中的 `DATABASE_URL`

### Q: 端口 8000 被占用

**解决方案：**

```bash
# 使用其他端口
python -m uvicorn main:app --reload --port 8001
```

## 生产环境部署

### 使用 Gunicorn (Linux)

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 使用 Docker

创建 `Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建和运行：

```bash
docker build -t treehole-api .
docker run -p 8000:8000 treehole-api
```

## 开发建议

1. **使用虚拟环境**

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

2. **代码格式化**

```bash
pip install black
black .
```

3. **类型检查**

```bash
pip install mypy
mypy app/
```

## 测试 API

### 使用 curl

参考 `API_EXAMPLES.md` 中的示例。

### 使用 Postman

1. 导入 Swagger 文档：http://localhost:8000/openapi.json
2. 创建环境变量 `base_url` = `http://localhost:8000/api/v1`
3. 创建环境变量 `token` 用于存储登录后的 JWT

### 使用 Python requests

```python
import requests

# 登录
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={"device_id": "test-device"}
)
token = response.json()["access_token"]

# 发布帖子
response = requests.post(
    "http://localhost:8000/api/v1/posts",
    headers={"Authorization": f"Bearer {token}"},
    json={"content": "测试帖子", "tag": "test"}
)
print(response.json())
```

## 数据库迁移

如果修改了数据库模型，需要重新创建数据库：

```bash
# 删除旧数据库
rm treehole.db  # Linux/Mac
del treehole.db  # Windows

# 重启服务，会自动创建新数据库
python run.py
```

**注意：** 生产环境建议使用 Alembic 进行数据库迁移。
