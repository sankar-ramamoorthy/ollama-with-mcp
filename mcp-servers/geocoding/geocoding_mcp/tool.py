# geocoding_mcp/tool.py
from geocoding_mcp.mcp_clients import geocode_address
import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("geocoding-mcp")

async def geocode_location(address: str):
    """
    Geocode a location using an external geocoding API (e.g., Nominatim).
    
    Args:
        address (str): The address to geocode.

    Returns:
        dict: Geocoding result containing latitude, longitude, etc.
    """
    if not address:
        return {"error": "Address is required"}

    # Call the geocoding client to get coordinates for the address
    result = await geocode_address(address)

    if "error" in result:
        return {"error": result["error"]}

    return {
        "address": result.get("address"),
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
        "country": result.get("country"),
        "city": result.get("city"),
        "state": result.get("state")
    }
