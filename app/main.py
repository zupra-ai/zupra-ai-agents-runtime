from fastapi import FastAPI, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.clients.redis_client import redis_client
from app.routes.tools.controller import router as tools_router
from app.routes.threads.controller import router as threads_router
from app.routes.agents.controller import router as agents_router


app = FastAPI(
    title="Zupra.AI AGENTS-RUNTIME",
    description="""### API specifications\n
                this is MD Text
              """,
    version="1.0",
)

class Utf8Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

app.include_router(router=tools_router, prefix="/v1")
app.include_router(router=threads_router, prefix="/v1")
app.include_router(router=agents_router, prefix="/v1")


