import httpx
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

DEFAULT_MODEL = "granite4:350m"


async def chat_with_ollama(message: str, model_name: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """
    Send a message to an Ollama model running on the HOST.
    Allows custom model names; defaults to Granite 350M.
    """
    payload = {
        "model": model_name,
        "prompt": message,
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            logger.info(f"[Ollama] Raw response: {data}")
            return {"message": data.get("response", "")}

    except Exception as e:
        logger.error(f"[Ollama] Error contacting Ollama: {e}")
        return {"error": f"Ollama request failed: {str(e)}"}
