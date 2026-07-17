from fastapi.responses import Response
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST


def register_metrics(app):

    @app.get("/metrics")
    async def metrics():

        return Response(
            content=generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )

