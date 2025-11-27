from backend.models.chat import ChatRequest, ChatResponse
from backend.services.ollama_service import chat_with_ollama

def chat_reply(request: ChatRequest) -> ChatResponse:
    """
    Use the Ollama service to get a reply to the chat request.
    """
    # Call the LLM (stub for now)
    response_data = chat_with_ollama(request.message)
    
    return ChatResponse(
        response=response_data.get("message", "No response from Ollama")
    )
