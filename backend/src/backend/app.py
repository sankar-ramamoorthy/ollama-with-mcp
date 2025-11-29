# backend/src/backend/app.py
from fastapi import FastAPI
from backend.routers.health import router as health_router
from backend.routers.chat import router as chat_router
from backend.routers.search import router as search_router
from backend.routers.weather import router as weather_router
from backend.routers.geocoding import router as geocoding_router
from backend.routers.datetime import router as datetime_router

app = FastAPI(title="Ollama with MCP Backend")

# Include routers
app.include_router(health_router)
app.include_router(chat_router)        # <-- updated chat endpoint
app.include_router(search_router)
app.include_router(weather_router)
app.include_router(geocoding_router)
app.include_router(datetime_router)
