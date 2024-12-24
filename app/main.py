from fastapi import FastAPI, HTTPException
from app.clients.redis_client import redis_client
from app.routes.tools.controller import router as tools_router

app = FastAPI()

app.include_router(router=tools_router, prefix="/v1")


