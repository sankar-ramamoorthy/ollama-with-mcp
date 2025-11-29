from fastapi import FastAPI
from backend.routers.health import router as health_router
from backend.routers.chat import router as chat_router
from backend.routers.search import router as search_router  # <-- new import
from backend.routers.weather import router as weather_router  # <-- new import

app = FastAPI()

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(search_router)  # <-- include MCP route
app.include_router(weather_router)  # <-- add this

