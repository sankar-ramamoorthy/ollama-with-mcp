# backend/src/backend/services/ollama_service.py
#a basic function in ollama_service.py that can call Ollama Granite

from typing import Dict, Any

# Stub function until real API is connected
def chat_with_ollama(message: str) -> Dict[str, Any]:
    """
    Send a message to the Ollama Granite model and return the response.
    """
    # TODO: Replace with actual Ollama API call
    response = {
        "message": f"Echo from Ollama (stub): {message}"
    }
    return response
