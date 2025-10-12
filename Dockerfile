# 使用 Python 3.13 官方镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制配置文件
COPY pyproject.toml alembic.ini ./

# 安装 Python 依赖
RUN pip install --no-cache-dir -e .

# 复制应用代码
COPY app/ ./app/
COPY migrate/ ./migrate/

# 设置环境变量
ENV DATABASE_URL="postgresql+asyncpg://yixin:yixin@localhost:5432/yixin" \
    MIGRATE_URL="postgresql+psycopg://yixin:yixin@localhost:5432/yixin"

# 创建非root用户
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]