import logging
from backend.models.chat import ChatRequest, ChatResponse
from backend.services.ollama_service import chat_with_ollama

logger = logging.getLogger(__name__)


async def chat_reply(request: ChatRequest) -> ChatResponse:
    """
    Use the Ollama service to get a reply to the chat request.
    """
    # Await the async Ollama call
    response_data = await chat_with_ollama(request.message)

    logger.info(f"[chat_reply] Received from Ollama: {response_data}")

    # response_data from the real API uses the key "message"
    return ChatResponse(
        response=response_data.get("message", "No response from Ollama")
    )
