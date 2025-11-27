from fastapi import APIRouter
from backend.models.chat import ChatRequest, ChatResponse
from backend.services.chat_service import chat_reply

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return await chat_reply(request)
