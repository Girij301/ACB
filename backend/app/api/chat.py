from fastapi import APIRouter
from app.models.chatmodels import ChatRequest, ChatResponse
from app.services.gemini_service import GeminiService

router = APIRouter()

service = GeminiService()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    reply = service.generate_response(request.message)

    return ChatResponse(response=reply)