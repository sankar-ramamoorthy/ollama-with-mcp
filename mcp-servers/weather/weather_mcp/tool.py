# weather_mcp/tool.py

from weather_mcp.mcp_clients import call_geocoding  # Import geocoding call (you will create this function)
import openmeteo_requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather-mcp")

async def get_weather(location: str):
    """
    Get weather for a location via geocoding and Open-Meteo.
    Returns structured JSON: {"location": str, "temperature": str, "condition": str, "source": str}
    """

    if not location or not isinstance(location, str):
        return {
            "location": location or "unknown",
            "temperature": "N/A",
            "condition": "N/A",
            "source": "Open-Meteo",
            "error": "Invalid location input"
        }

    # Step 1: Call geocoding MCP to get latitude and longitude
    geocode_result = await call_geocoding(location)

    if "error" in geocode_result:
        return {
            "location": location,
            "temperature": "N/A",
            "condition": "N/A",
            "source": "Open-Meteo",
            "error": geocode_result["error"]
        }

    # Assuming geocoding response has lat and lon
    latitude = geocode_result.get("latitude")
    longitude = geocode_result.get("longitude")

    if not latitude or not longitude:
        return {
            "location": location,
            "temperature": "N/A",
            "condition": "N/A",
            "source": "Open-Meteo",
            "error": "Geocoding failed to return valid coordinates"
        }

    # Step 2: Call Open-Meteo API with coordinates
    try:
        openmeteo = openmeteo_requests.AsyncClient()
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m"],
        }

        # Fetch weather data
        responses = await openmeteo.weather_api(url, params=params)

        # Process first response (assuming single response)
        response = responses[0]
        current_temperature_2m = response.Current().Variables(0).Value()
        current_humidity_2m = response.Current().Variables(1).Value()

        # Build the response
        return {
            "location": location,
            "temperature": f"{current_temperature_2m}°C",
            "condition": "N/A",  # Modify this if you want specific weather conditions
            "source": "Open-Meteo",
            "humidity": f"{current_humidity_2m}%",
        }

    except Exception as e:
        logger.error(f"Error fetching weather for {location}: {e}")
        return {
            "location": location,
            "temperature": "N/A",
            "condition": "N/A",
            "source": "Open-Meteo",
            "error": str(e)
        }
