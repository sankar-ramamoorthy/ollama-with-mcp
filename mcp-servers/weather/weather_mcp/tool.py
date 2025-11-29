# weather_mcp/tool.py
#from backend.mcp_clients import call_searchxng
# weather_mcp/tool.py
from weather_mcp.mcp_clients import call_searchxng
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weather-mcp")
 
async def get_weather(location: str):
    """
    Get weather for a location via SearchXNG.
    Returns structured JSON: {"location": str, "temperature": str, "condition": str, "source": str}
    """
    if not location or not isinstance(location, str):
        return {
            "location": location or "unknown",
            "temperature": "N/A",
            "condition": "N/A",
            "source": "SearchXNG",
            "error": "Invalid location input"
        }

    query = f"current weather in {location}"
    try:
        search_result = await call_searchxng(query)
        # Print the entire result to inspect it
        print("Search result:", search_result)
        # Example: Extract simple weather info from search result content
        # For now, we keep it simple; later you can parse structured text
        content = search_result.get("results") or search_result.get("content") or "N/A"

        # Fallback to basic placeholder if parsing fails
        temperature = "N/A"
        condition = "N/A"
        if isinstance(content, list):
            text_items = [item.get("text") for item in content if isinstance(item, dict) and "text" in item]
            combined_text = " ".join(text_items)
            # VERY basic parsing placeholder
            if "°" in combined_text:
                temperature = combined_text.split("°")[0] + "°"
            if "cloud" in combined_text.lower():
                condition = "Cloudy"
            elif "rain" in combined_text.lower():
                condition = "Rainy"

        return {
            "location": location,
            "temperature": temperature,
            "condition": condition,
            "source": "SearchXNG"
        }

    except Exception as e:
        logger.error(f"Error fetching weather for {location}: {e}")
        return {
            "location": location,
            "temperature": "N/A",
            "condition": "N/A",
            "source": "SearchXNG",
            "error": str(e)
        }



