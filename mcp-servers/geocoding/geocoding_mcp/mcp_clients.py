import time
import asyncio
from typing import Any, Dict
import httpx
import logging

GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search"
logger = logging.getLogger("geocoding-mcp")

_last_request_time = 0.0
_rate_limit_lock = asyncio.Lock()

async def geocode_address(address: str) -> Dict[str, Any]:
    global _last_request_time

    if not address:
        return {"error": "Address is required"}

    # --- Async rate limiting ---
    async with _rate_limit_lock:
        now = time.time()
        elapsed = now - _last_request_time
        if elapsed < 1.0:
            await asyncio.sleep(1.0 - elapsed)
        _last_request_time = time.time()
    # ---------------------------

    params = {
        "q": address,
        "format": "json",
        "addressdetails": 1
    }

    headers = {
        "Referer": "https://github.com/sankar-ramamoorthy/ollama-with-mcp"
    }

    try:
        async with httpx.AsyncClient(headers=headers, timeout=10) as client:
            response = await client.get(GEOCODING_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if data:
                first_result = data[0]
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
