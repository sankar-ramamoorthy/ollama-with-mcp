from fastapi import FastAPI
from backend.routers.health import router as health_router
from backend.routers.chat import router as chat_router
from backend.routers.search import router as search_router
from backend.routers.weather import router as weather_router  # <-- existing import
from backend.routers.geocoding import router as geocoding_router  # <-- new import
from backend.routers.datetime import router as datetime_router  # <-- new import

app = FastAPI()

# Include all the routers
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(search_router)  # existing MCP route
app.include_router(weather_router)  # existing weather MCP route
app.include_router(geocoding_router)  # <-- include geocoding MCP route
app.include_router(datetime_router)  # <-- include datetime MCP route
