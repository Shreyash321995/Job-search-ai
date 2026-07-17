import time

from prometheus_client import Counter
from prometheus_client import Histogram

http_requests = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

request_latency = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ["endpoint"]
)


def register_middleware(app):

    @app.middleware("http")
    async def metrics_middleware(request, call_next):

        start = time.time()

        response = await call_next(request)

        duration = time.time() - start

        http_requests.labels(
            request.method,
            request.url.path
        ).inc()

        request_latency.labels(
            request.url.path
        ).observe(duration)

        return response
