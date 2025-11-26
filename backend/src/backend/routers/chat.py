from fastapi import APIRouter
from backend.models.chat import ChatRequest, ChatResponse
from backend.services.chat_service import chat_reply

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return chat_reply(request)
