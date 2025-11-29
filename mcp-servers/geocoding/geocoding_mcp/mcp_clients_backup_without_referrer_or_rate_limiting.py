from typing import Any, Dict
import httpx
import logging

# Geocoding API endpoint (e.g., OpenStreetMap Nominatim)
GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search"
# Set up a logger
logger = logging.getLogger("geocoding-mcp")

async def geocode_address(address: str) -> Dict[str, Any]:
    """
    Geocode an address using OpenStreetMap's Nominatim API.
    
    Args:
        address (str): The address to geocode.

    Returns:
        dict: A dictionary containing geocoding information (latitude, longitude, etc.)
    """
    if not address:
        return {"error": "Address is required"}

    # Prepare the query parameters
    params = {
        "q": address,
        "format": "json",
        "addressdetails": 1
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(GEOCODING_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if data:
                # Extract the relevant data from the response
                first_result = data[0]  # Take the first result
                return {
                    "address": first_result.get("display_name"),
                    "latitude": first_result.get("lat"),
                    "longitude": first_result.get("lon"),
                    "country": first_result.get("address", {}).get("country"),
                    "city": first_result.get("address", {}).get("city"),
                    "state": first_result.get("address", {}).get("state")
                }
            else:
                return {"error": "No geocoding results found"}

    except Exception as e:
        logger.error(f"Error geocoding address '{address}': {e}")
        return {"error": f"Error: {e}"}
