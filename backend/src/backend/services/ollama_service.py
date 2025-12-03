import httpx
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://host.docker.internal:11434/api/generate"

DEFAULT_MODEL = "Qwen3:4b"


async def chat_with_ollama(message: str, model_name: str = DEFAULT_MODEL) -> Dict[str, Any]:
    """
    Send a message to an Ollama model running on the HOST.
    Allows custom model names; defaults to Qwen3:4b.
    """
    payload = {
        "model": model_name,
        "prompt": message,
        "stream": False
    }
    print("In chat with ollama")
    print("In chat with ollama model",model_name)

    try:
        async with httpx.AsyncClient(timeout=2000.0) as client:
            print("chat with ollama About to post")
            response = await client.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            print("chat with ollama data = response.json()",data)

            logger.info(f"[Ollama] Raw response: {data}")
            return {"message": data.get("response", "")}

    except Exception as e:
        logger.error(f"[Ollama] Error contacting Ollama: {e}")
        return {"error": f"Ollama request failed: {str(e)}"}
