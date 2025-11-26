from fastapi import FastAPI
from backend.routers.health import router as health_router
from backend.routers.chat import router as chat_router

app = FastAPI()

app.include_router(health_router)
app.include_router(chat_router)
