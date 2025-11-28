# searchxng_mcp/tool.py
import httpx
from typing import List, Dict, Any

SEARCHXNG_API_URL = "http://searchxng_svc:8080/search"  # internal container URL

async def search_web(query: str) -> List[Dict[str, Any]]:
    if not query or not isinstance(query, str):
        return []

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                SEARCHXNG_API_URL,
                params={"q": query, "format": "json"}
            )
            resp.raise_for_status()
            data = resp.json()
            results = [{"title": r.get("title"), "url": r.get("url")} for r in data.get("results", [])]
            return results
    except Exception as e:
        return [{"title": f"Error: {e}", "url": ""}]
