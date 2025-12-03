import logging
from backend.models.chat import ChatRequest, ChatResponse
from backend.services.ollama_service import chat_with_ollama

logger = logging.getLogger(__name__)
DEFAULT_MODEL = "Qwen3:4b"

async def chat_reply(request: ChatRequest,model_name: str = DEFAULT_MODEL) -> ChatResponse:
    """
    Use the Ollama service to get a reply to the chat request.
    """
    # Await the async Ollama call
    response_data = await chat_with_ollama(request.message,model_name)

    logger.info(f"[chat_reply] Received from Ollama: {response_data}")

    # response_data from the real API uses the key "message"
    return ChatResponse(
        response=response_data.get("message", "No response from Ollama")
    )
