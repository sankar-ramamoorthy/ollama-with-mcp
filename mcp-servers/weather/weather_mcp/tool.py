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

            # ---- DAILY ----
            "daily": [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "apparent_temperature_max",
                "apparent_temperature_min",
                "sunrise",
                "sunset",
                "daylight_duration",
                "sunshine_duration",
                "uv_index_max",
                "uv_index_clear_sky_max",
                "rain_sum",
                "showers_sum",
                "snowfall_sum",
                "precipitation_sum",
                "precipitation_hours",
                "precipitation_probability_max",
                "wind_speed_10m_max",
                "wind_gusts_10m_max",
                "wind_direction_10m_dominant",
                "shortwave_radiation_sum",
                "et0_fao_evapotranspiration",
            ],

            # ---- HOURLY ----
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "rain",
                "snowfall",
                "weather_code",
                "cloud_cover",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m",
                "uv_index",
                "uv_index_clear_sky",
            ],
        }

        responses = await client.weather_api(url, params=params)
        r = responses[0]

        current = r.Current()
        daily = r.Daily()
        hourly = r.Hourly()

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
        # EXTRACT DAILY (first index)
        # -----------------------------------------
        day = DailyWeather(
            weather_code=int(daily.Variables(0).ValuesAsNumpy()[0]),
            temperature_2m_max=daily.Variables(1).ValuesAsNumpy()[0],
            temperature_2m_min=daily.Variables(2).ValuesAsNumpy()[0],
            apparent_temperature_max=daily.Variables(3).ValuesAsNumpy()[0],
            apparent_temperature_min=daily.Variables(4).ValuesAsNumpy()[0],
            sunrise=daily.Variables(5).ValuesAsNumpy()[0],
            sunset=daily.Variables(6).ValuesAsNumpy()[0],
            daylight_duration=daily.Variables(7).ValuesAsNumpy()[0],
            sunshine_duration=daily.Variables(8).ValuesAsNumpy()[0],
            uv_index_max=daily.Variables(9).ValuesAsNumpy()[0],
            uv_index_clear_sky_max=daily.Variables(10).ValuesAsNumpy()[0],
            rain_sum=daily.Variables(11).ValuesAsNumpy()[0],
            showers_sum=daily.Variables(12).ValuesAsNumpy()[0],
            snowfall_sum=daily.Variables(13).ValuesAsNumpy()[0],
            precipitation_sum=daily.Variables(14).ValuesAsNumpy()[0],
            precipitation_hours=daily.Variables(15).ValuesAsNumpy()[0],
            precipitation_probability_max=daily.Variables(16).ValuesAsNumpy()[0],
            wind_speed_10m_max=daily.Variables(17).ValuesAsNumpy()[0],
            wind_gusts_10m_max=daily.Variables(18).ValuesAsNumpy()[0],
            wind_direction_10m_dominant=daily.Variables(19).ValuesAsNumpy()[0],
            shortwave_radiation_sum=daily.Variables(20).ValuesAsNumpy()[0],
            et0_fao_evapotranspiration=daily.Variables(21).ValuesAsNumpy()[0],
        )

        # -----------------------------------------
        # EXTRACT HOURLY FORECAST
        # -----------------------------------------
        hourly_weather = HourlyWeather(
            time=[t.isoformat() for t in hourly.Time()],
            temperature_2m=hourly.Variables(0).ValuesAsNumpy().tolist(),
            relative_humidity_2m=hourly.Variables(1).ValuesAsNumpy().tolist(),
            apparent_temperature=hourly.Variables(2).ValuesAsNumpy().tolist(),
            precipitation=hourly.Variables(3).ValuesAsNumpy().tolist(),
            rain=hourly.Variables(4).ValuesAsNumpy().tolist(),
            snowfall=hourly.Variables(5).ValuesAsNumpy().tolist(),
            weather_code=hourly.Variables(6).ValuesAsNumpy().tolist(),
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

        return validated.model_dump()

    except Exception as e:
        logger.error(f"Weather MCP error: {e}")
        return {"error": str(e)}
