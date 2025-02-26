# app/security.py
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, limit=5):
        super().__init__(app)
        self.limit = limit
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        self.requests[client_ip] = self.requests.get(client_ip, 0) + 1
        if self.requests[client_ip] > self.limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        return await call_next(request)


rate_limiter = RateLimiter
