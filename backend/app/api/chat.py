from app.core.logger import logger
from app.models.chatmodels import ChatRequest, ChatResponse
from app.services.gemini_service import GeminiService
from fastapi import APIRouter

router = APIRouter()

service = GeminiService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    logger.info(f"Incoming request: {request.message}")

    reply = service.generate_response(request.message)

    logger.info("Request processed successfully")

    return ChatResponse(
        success=True,
        message="Response generated successfully",
        data={
            "response": reply
        },
        error=None
    )