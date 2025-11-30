# weather_mcp/tool.py

import time
import asyncio
import logging
from typing import List, Optional

import openmeteo_requests
from pydantic import BaseModel, Field

from weather_mcp.mcp_clients import call_geocoding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather-mcp")
print("weather weather_mpc tool.py")


# ============================================================
# RATE LIMITING (1 request / second)
# ============================================================

_last_request_ts = 0.0
_rate_limit_lock = asyncio.Lock()

async def enforce_rate_limit():
    global _last_request_ts
    async with _rate_limit_lock:
        now = time.time()
        elapsed = now - _last_request_ts
        if elapsed < 1.0:
            await asyncio.sleep(1.0 - elapsed)
        _last_request_ts = time.time()


# ============================================================
# Pydantic MODELS FOR STRUCTURED WEATHER
# ============================================================

class CurrentWeather(BaseModel):
    temperature_2m: float
    relative_humidity_2m: float
    apparent_temperature: float
    is_day: bool
    precipitation: float
    rain: float
    showers: float
    snowfall: float
    weather_code: int
    cloud_cover: float
    pressure_msl: float
    surface_pressure: float
    wind_speed_10m: float
    wind_direction_10m: float
    wind_gusts_10m: float




class WeatherResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    current: CurrentWeather
    source: str = "Open-Meteo"


# ============================================================
# MAIN WEATHER FUNCTION
# ============================================================

async def get_weather(location: str) -> dict:
    """Get weather using geocoding MCP + Open-Meteo."""

    if not location or not isinstance(location, str):
        return {"error": "Invalid location input"}

    # -----------------------------------------
    # 1. GEOCODE LOCATION
    # -----------------------------------------
    geocode = await call_geocoding(location)
    if "error" in geocode:
        return {"error": geocode["error"]}

    latitude = geocode.get("latitude")
    longitude = geocode.get("longitude")

    if not latitude or not longitude:
        return {"error": "Geocoding returned no coordinates"}

    # -----------------------------------------
    # 2. RATE LIMIT
    # -----------------------------------------
    await enforce_rate_limit()

    # -----------------------------------------
    # 3. OPEN-METEO REQUEST
    # -----------------------------------------
    try:
        client = openmeteo_requests.AsyncClient()
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,

            # ---- CURRENT ----
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "is_day",
                "precipitation",
                "rain",
                "showers",
                "snowfall",
                "weather_code",
                "cloud_cover",
                "pressure_msl",
                "surface_pressure",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m",
            ],
        }

        responses = await client.weather_api(url, params=params)
        r = responses[0]

        current = r.Current()
        #daily = r.Daily()
        #hourly = r.Hourly()

        # -----------------------------------------
        # EXTRACT CURRENT
        # -----------------------------------------
        curr = CurrentWeather(
            temperature_2m=current.Variables(0).Value(),
            relative_humidity_2m=current.Variables(1).Value(),
            apparent_temperature=current.Variables(2).Value(),
            is_day=bool(current.Variables(3).Value()),
            precipitation=current.Variables(4).Value(),
            rain=current.Variables(5).Value(),
            showers=current.Variables(6).Value(),
            snowfall=current.Variables(7).Value(),
            weather_code=int(current.Variables(8).Value()),
            cloud_cover=current.Variables(9).Value(),
            pressure_msl=current.Variables(10).Value(),
            surface_pressure=current.Variables(11).Value(),
            wind_speed_10m=current.Variables(12).Value(),
            wind_direction_10m=current.Variables(13).Value(),
            wind_gusts_10m=current.Variables(14).Value(),
        )

        # -----------------------------------------
        # MODEL VALIDATION & RETURN
        # -----------------------------------------
        validated = WeatherResponse(
            location=location,
            latitude=float(latitude),
            longitude=float(longitude),
            current=curr,
        )

        return validated.model_dump()

    except Exception as e:
        logger.error(f"Weather MCP error: {e}")
        return {"error": str(e)}
