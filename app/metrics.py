"""应用指标定义"""

from prometheus_client import Counter, Histogram

# 总请求数
requests_total = Counter(
    "app_requests_total",
    "Total number of requests",
    ["method", "endpoint", "http_status"],
)

# 请求延迟（毫秒）
requests_latency = Histogram(
    "app_requests_latency",
    "Request latency (ms)",
    ["method", "endpoint"],
    buckets=[50, 100, 200, 300, 400, 500, 750, 1000],
)
