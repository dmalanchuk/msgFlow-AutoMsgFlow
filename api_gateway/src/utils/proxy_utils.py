from fastapi import Request, Response
import httpx


async def proxy_request(request: Request, url: str) -> Response:
    """General query proxy func to target url"""

    body = await request.body()

    # Копіюємо заголовки
    headers = dict(request.headers)

    user_email = getattr(request.state, "user_email", None)
    if user_email:
        headers["X-User-Email"] = user_email

    print(f"[GATEWAY] Proxying request to: {url}, with X-User-Email: {user_email}")
    async with httpx.AsyncClient() as client:
        proxy_response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            params=request.query_params
        )

    return Response(
        content=proxy_response.content,
        status_code=proxy_response.status_code,
        headers=proxy_response.headers
    )
