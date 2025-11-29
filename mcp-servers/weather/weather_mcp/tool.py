# weather_mcp/tool.py

from weather_mcp.mcp_clients import call_geocoding
import openmeteo_requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather-mcp")


async def get_weather(location: str):
    """
    Get weather for a location using:
    1. Geocoding MCP (to get lat/lon)
    2. Open-Meteo Forecast API (current + daily)

    Returns structured JSON ready for an LLM.
    """

    # --------------------------
    # Validate input
    # --------------------------
    if not location or not isinstance(location, str):
        return {
            "location": location or "unknown",
            "error": "Invalid location input",
            "source": "Open-Meteo",
        }

    # --------------------------
    # Step 1: Geocode the location
    # --------------------------
    geocode_result = await call_geocoding(location)

    if "error" in geocode_result:
        return {
            "location": location,
            "error": geocode_result["error"],
            "source": "Open-Meteo",
        }

    latitude = geocode_result.get("latitude")
    longitude = geocode_result.get("longitude")

    if not latitude or not longitude:
        return {
            "location": location,
            "error": "Geocoding failed to return valid coordinates",
            "source": "Open-Meteo",
        }

    # --------------------------
    # Step 2: Call Open-Meteo
    # --------------------------
    try:
        openmeteo = openmeteo_requests.AsyncClient()
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,

            # FULL CURRENT CONDITIONS
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

            # FULL DAILY FORECAST
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
        }

        responses = await openmeteo.weather_api(url, params=params)
        response = responses[0]  # Open-Meteo always returns a list

        current = response.Current()
        daily = response.Daily()

        # --------------------------
        # Extract CURRENT weather
        # --------------------------
        curr = {
            "temperature_2m": current.Variables(0).Value(),
            "relative_humidity_2m": current.Variables(1).Value(),
            "apparent_temperature": current.Variables(2).Value(),
            "is_day": bool(current.Variables(3).Value()),
            "precipitation": current.Variables(4).Value(),
            "rain": current.Variables(5).Value(),
            "showers": current.Variables(6).Value(),
            "snowfall": current.Variables(7).Value(),
            "weather_code": current.Variables(8).Value(),
            "cloud_cover": current.Variables(9).Value(),
            "pressure_msl": current.Variables(10).Value(),
            "surface_pressure": current.Variables(11).Value(),
            "wind_speed_10m": current.Variables(12).Value(),
            "wind_direction_10m": current.Variables(13).Value(),
            "wind_gusts_10m": current.Variables(14).Value(),
        }

        # --------------------------
        # Extract DAILY weather
        # --------------------------
        day = {
            "weather_code":                daily.Variables(0).ValuesAsNumpy()[0],
            "temperature_2m_max":          daily.Variables(1).ValuesAsNumpy()[0],
            "temperature_2m_min":          daily.Variables(2).ValuesAsNumpy()[0],
            "apparent_temperature_max":    daily.Variables(3).ValuesAsNumpy()[0],
            "apparent_temperature_min":    daily.Variables(4).ValuesAsNumpy()[0],
            "sunrise":                     daily.Variables(5).ValuesAsNumpy()[0],
            "sunset":                      daily.Variables(6).ValuesAsNumpy()[0],
            "daylight_duration":           daily.Variables(7).ValuesAsNumpy()[0],
            "sunshine_duration":           daily.Variables(8).ValuesAsNumpy()[0],
            "uv_index_max":                daily.Variables(9).ValuesAsNumpy()[0],
            "uv_index_clear_sky_max":      daily.Variables(10).ValuesAsNumpy()[0],
            "rain_sum":                    daily.Variables(11).ValuesAsNumpy()[0],
            "showers_sum":                 daily.Variables(12).ValuesAsNumpy()[0],
            "snowfall_sum":                daily.Variables(13).ValuesAsNumpy()[0],
            "precipitation_sum":           daily.Variables(14).ValuesAsNumpy()[0],
            "precipitation_hours":         daily.Variables(15).ValuesAsNumpy()[0],
            "precipitation_probability_max": daily.Variables(16).ValuesAsNumpy()[0],
            "wind_speed_10m_max":          daily.Variables(17).ValuesAsNumpy()[0],
            "wind_gusts_10m_max":          daily.Variables(18).ValuesAsNumpy()[0],
            "wind_direction_10m_dominant": daily.Variables(19).ValuesAsNumpy()[0],
            "shortwave_radiation_sum":     daily.Variables(20).ValuesAsNumpy()[0],
            "et0_fao_evapotranspiration":  daily.Variables(21).ValuesAsNumpy()[0],
        }

        # --------------------------
        # Return everything cleanly
        # --------------------------
        return {
            "location": location,
            "latitude": latitude,
            "longitude": longitude,
            "current": curr,
            "daily": day,
            "source": "Open-Meteo",
        }

    except Exception as e:
        logger.error(f"Error fetching weather for {location}: {e}")
        return {
            "location": location,
            "error": str(e),
            "source": "Open-Meteo",
        }
