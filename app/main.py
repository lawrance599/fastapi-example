from fastapi import FastAPI
from .routers import user
from .metrics import requests_total, requests_latency

app = FastAPI()
app.include_router(user.router)


# 性能指标中间件
@app.middleware("http")
async def metrics_middleware(request, call_next):
    import time

    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # 毫秒
    requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code,
    ).inc()
    requests_latency.labels(
        method=request.method, endpoint=request.url.path
    ).observe(process_time)
    return response


# 性能指标路由
@app.get("/metrics")
async def metrics():
    from prometheus_client import (
        generate_latest,
        CONTENT_TYPE_LATEST,
    )
    from fastapi.responses import Response

    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
