import os

import httpx
from fastapi import FastAPI, Request, Response

app = FastAPI()

POSTS_SERVICE_URL = os.getenv("POSTS_SERVICE_URL")
CATEGORIES_SERVICE_URL = os.getenv("CATEGORIES_SERVICE_URL")

client = httpx.AsyncClient()


@app.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
)
async def proxy_request(request: Request, path: str):
    """
    Эта функция определяет, какому сервису перенаправить запрос,
    основываясь на начальной части URL-пути.
    """
    target_url = None

    if path.startswith("posts"):
        target_url = f"{POSTS_SERVICE_URL}/{path}"
    elif path.startswith("categories"):
        target_url = f"{CATEGORIES_SERVICE_URL}/{path}"

    if not target_url:
        return Response(content="Not Found", status_code=404)

    body = await request.body()

    proxied_req = client.build_request(
        method=request.method,
        url=target_url,
        headers=request.headers,
        params=request.query_params,
        content=body,
    )

    response = await client.send(proxied_req)

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )
