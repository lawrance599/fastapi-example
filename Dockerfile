# 使用 Python 3.13 官方镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 设置 pip 使用国内源
ENV PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"\
    PIP_TRUSTED_HOST="pypi.tuna.tsinghua.edu.cn"\
    UV_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"

# 安装系统依赖（使用国内镜像源）
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 通过 pip 安装 uv
RUN pip install --no-cache-dir uv

# 设置 uv 使用国内源

COPY pyproject.toml alembic.ini entrypoint.sh ./

# 使用 uv 安装 Python 依赖
RUN uv sync --no-cache

# 复制应用代码和依赖
COPY app/ ./app/
COPY migrate/ ./migrate/


# 创建非root用户
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app && \
    chmod +x entrypoint.sh
USER appuser
# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["./entrypoint.sh"]