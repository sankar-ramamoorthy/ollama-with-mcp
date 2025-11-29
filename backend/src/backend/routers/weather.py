# backend/src/backend/routers/weather.py
from fastapi import APIRouter, HTTPException
from backend.mcp_clients import call_weather
from pydantic import BaseModel

router = APIRouter(prefix="/weather", tags=["weather"])

class WeatherRequest(BaseModel):
    location: str

@router.post("/get")
async def get_weather(request: WeatherRequest):
    """
    Call the Weather MCP tool for a given location.
    """
    result = await call_weather(request.location)
    
    if not result or "error" in result:
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    
    return result
