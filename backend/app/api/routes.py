from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.chat_service import chat_reply


router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    """AI와 대화하는 기본 챗 엔드포인트"""
    reply = chat_reply(payload.message)
    return ChatResponse(reply=reply)
