# weather_mcp/tool.py

import time
import asyncio
import logging
from typing import List, Optional
import numpy as np

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

class DailyWeather(BaseModel):
    weather_code: int
    temperature_2m_max: float
    temperature_2m_min: float
    apparent_temperature_max: float
    apparent_temperature_min: float
    sunrise: float
    sunset: float
    daylight_duration: float
    sunshine_duration: float
    uv_index_max: float
    uv_index_clear_sky_max: float
    rain_sum: float
    showers_sum: float
    snowfall_sum: float
    precipitation_sum: float
    precipitation_hours: float
    precipitation_probability_max: float
    wind_speed_10m_max: float
    wind_gusts_10m_max: float
    wind_direction_10m_dominant: float
    shortwave_radiation_sum: float
    et0_fao_evapotranspiration: float

class HourlyWeather(BaseModel):
    time: List[str] = Field(default_factory=list)
    temperature_2m: List[float]
    relative_humidity_2m: List[float]
    apparent_temperature: List[float]
    precipitation: List[float]
    rain: List[float]
    snowfall: List[float]
    weather_code: List[int]
    cloud_cover: List[float]
    wind_speed_10m: List[float]
    wind_direction_10m: List[float]
    wind_gusts_10m: List[float]
    uv_index: List[float]
    uv_index_clear_sky: List[float]

class WeatherResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    current: CurrentWeather
    daily: DailyWeather
    hourly: HourlyWeather
    source: str = "Open-Meteo"

# ============================================================
# SAFE DATA EXTRACTION HELPER
# ============================================================

def safe_extract(var_data, index=0, default_float=0.0, default_int=0):
    """Safely extract value from numpy array or scalar."""
    try:
        if hasattr(var_data, '__len__') and len(var_data) > index:
            return float(var_data[index]) if default_float else int(var_data[index])
        return float(var_data) if default_float else int(var_data)
    except (IndexError, TypeError):
        return default_float if default_float else default_int

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

    logger.info(f"Geocoded {location} -> lat:{latitude}, lon:{longitude}")

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
                "temperature_2m", "relative_humidity_2m", "apparent_temperature",
                "is_day", "precipitation", "rain", "showers", "snowfall",
                "weather_code", "cloud_cover", "pressure_msl", "surface_pressure",
                "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m",
            ],
            # ---- DAILY ----
            "daily": [
                "weather_code", "temperature_2m_max", "temperature_2m_min",
                "apparent_temperature_max", "apparent_temperature_min",
                "sunrise", "sunset", "daylight_duration", "sunshine_duration",
                "uv_index_max", "uv_index_clear_sky_max", "rain_sum", "showers_sum",
                "snowfall_sum", "precipitation_sum", "precipitation_hours",
                "precipitation_probability_max", "wind_speed_10m_max",
                "wind_gusts_10m_max", "wind_direction_10m_dominant",
                "shortwave_radiation_sum", "et0_fao_evapotranspiration",
            ],
            # ---- HOURLY ----
            "hourly": [
                "temperature_2m", "relative_humidity_2m", "apparent_temperature",
                "precipitation", "rain", "snowfall", "weather_code", "cloud_cover",
                "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m",
                "uv_index", "uv_index_clear_sky",
            ],
        }

        responses = await client.weather_api(url, params=params)
        print("response from meteo",responses)
        r = responses[0]

        current = r.Current()
        daily = r.Daily()
        hourly = r.Hourly()

        # -----------------------------------------
        # EXTRACT CURRENT - SAFE
        # -----------------------------------------
        curr = CurrentWeather(
            temperature_2m=float(current.Variables(0).Value()),
            relative_humidity_2m=float(current.Variables(1).Value()),
            apparent_temperature=float(current.Variables(2).Value()),
            is_day=bool(current.Variables(3).Value()),
            precipitation=float(current.Variables(4).Value()),
            rain=float(current.Variables(5).Value()),
            showers=float(current.Variables(6).Value()),
            snowfall=float(current.Variables(7).Value()),
            weather_code=int(current.Variables(8).Value()),
            cloud_cover=float(current.Variables(9).Value()),
            pressure_msl=float(current.Variables(10).Value()),
            surface_pressure=float(current.Variables(11).Value()),
            wind_speed_10m=float(current.Variables(12).Value()),
            wind_direction_10m=float(current.Variables(13).Value()),
            wind_gusts_10m=float(current.Variables(14).Value()),
        )

        # -----------------------------------------
        # EXTRACT DAILY - SAFE (THIS WAS CRASHING!)
        # -----------------------------------------
        day = DailyWeather(
            weather_code=safe_extract(daily.Variables(0).ValuesAsNumpy(), default_int=0),
            temperature_2m_max=safe_extract(daily.Variables(1).ValuesAsNumpy()),
            temperature_2m_min=safe_extract(daily.Variables(2).ValuesAsNumpy()),
            apparent_temperature_max=safe_extract(daily.Variables(3).ValuesAsNumpy()),
            apparent_temperature_min=safe_extract(daily.Variables(4).ValuesAsNumpy()),
            sunrise=safe_extract(daily.Variables(5).ValuesAsNumpy()),
            sunset=safe_extract(daily.Variables(6).ValuesAsNumpy()),
            daylight_duration=safe_extract(daily.Variables(7).ValuesAsNumpy()),
            sunshine_duration=safe_extract(daily.Variables(8).ValuesAsNumpy()),
            uv_index_max=safe_extract(daily.Variables(9).ValuesAsNumpy()),
            uv_index_clear_sky_max=safe_extract(daily.Variables(10).ValuesAsNumpy()),
            rain_sum=safe_extract(daily.Variables(11).ValuesAsNumpy()),
            showers_sum=safe_extract(daily.Variables(12).ValuesAsNumpy()),
            snowfall_sum=safe_extract(daily.Variables(13).ValuesAsNumpy()),
            precipitation_sum=safe_extract(daily.Variables(14).ValuesAsNumpy()),
            precipitation_hours=safe_extract(daily.Variables(15).ValuesAsNumpy()),
            precipitation_probability_max=safe_extract(daily.Variables(16).ValuesAsNumpy()),
            wind_speed_10m_max=safe_extract(daily.Variables(17).ValuesAsNumpy()),
            wind_gusts_10m_max=safe_extract(daily.Variables(18).ValuesAsNumpy()),
            wind_direction_10m_dominant=safe_extract(daily.Variables(19).ValuesAsNumpy()),
            shortwave_radiation_sum=safe_extract(daily.Variables(20).ValuesAsNumpy()),
            et0_fao_evapotranspiration=safe_extract(daily.Variables(21).ValuesAsNumpy()),
        )

        # -----------------------------------------
        # EXTRACT HOURLY FORECAST - SAFE
        # -----------------------------------------
        hourly_vars = hourly.Variables(0).ValuesAsNumpy()
        hourly_weather = HourlyWeather(
            time=[t.isoformat() for t in hourly.Time()],
            temperature_2m=hourly.Variables(0).ValuesAsNumpy().tolist(),
            relative_humidity_2m=hourly.Variables(1).ValuesAsNumpy().tolist(),
            apparent_temperature=hourly.Variables(2).ValuesAsNumpy().tolist(),
            precipitation=hourly.Variables(3).ValuesAsNumpy().tolist(),
            rain=hourly.Variables(4).ValuesAsNumpy().tolist(),
            snowfall=hourly.Variables(5).ValuesAsNumpy().tolist(),
            weather_code=[int(x) for x in hourly.Variables(6).ValuesAsNumpy()],
            cloud_cover=hourly.Variables(7).ValuesAsNumpy().tolist(),
            wind_speed_10m=hourly.Variables(8).ValuesAsNumpy().tolist(),
            wind_direction_10m=hourly.Variables(9).ValuesAsNumpy().tolist(),
            wind_gusts_10m=hourly.Variables(10).ValuesAsNumpy().tolist(),
            uv_index=hourly.Variables(11).ValuesAsNumpy().tolist(),
            uv_index_clear_sky=hourly.Variables(12).ValuesAsNumpy().tolist(),
        )

        # -----------------------------------------
        # MODEL VALIDATION & RETURN
        # -----------------------------------------
        validated = WeatherResponse(
            location=location,
            latitude=float(latitude),
            longitude=float(longitude),
            current=curr,
            daily=day,
            hourly=hourly_weather,
        )

        logger.info(f"Weather fetched successfully for {location}")
        return validated.model_dump()

    except Exception as e:
        logger.error(f"Weather MCP error: {e}")
        return {"error": str(e)}
