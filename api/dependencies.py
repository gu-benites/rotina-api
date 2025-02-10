import httpx

async def get_http_client(timeout: float = 5.0) -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=timeout)
