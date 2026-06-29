from fastapi import APIRouter
from app.models.chatmodels import ChatRequest, ChatResponse
from app.services.gemini_service import GeminiService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    reply = GeminiService.generate_response(request.message)

    return ChatResponse(response=reply)