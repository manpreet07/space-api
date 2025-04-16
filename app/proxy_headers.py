from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class ProxyHeaderFixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "x-forwarded-proto" in request.headers:
            request.scope["scheme"] = request.headers["x-forwarded-proto"]
        return await call_next(request)
