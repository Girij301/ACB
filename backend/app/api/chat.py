from fastapi import APIRouter

from app.core.logger import logger
from app.models.chatmodels import ChatRequest, ChatResponse
from app.services.gemini_service import GeminiService
from app.services.memory import save_message, get_chat_history

router = APIRouter()

service = GeminiService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    logger.info(f"Incoming request: {request.message}")

    # Save the user's message
    save_message(
        session_id=request.session_id,
        role="user",
        content=request.message,
    )

    # Retrieve previous conversation
    history = get_chat_history(request.session_id)

    # Build prompt with conversation history
    conversation = (
    "You are a helpful AI assistant. "
    "Use the conversation history below to answer the user's latest message.\n\n"
    )

    for msg in history:
        conversation += f"{msg['role']}: {msg['content']}\n"

    conversation += "\nContinue the conversation naturally as the assistant."

    logger.info("Sending conversation history to Gemini")

    # Generate AI response
    reply = service.generate_response(conversation)

    # Save assistant response
    save_message(
        session_id=request.session_id,
        role="assistant",
        content=reply,
    )

    logger.info("Request processed successfully")

    return ChatResponse(
        success=True,
        message="Response generated successfully",
        data={
            "response": reply
        },
        error=None
    )