from fastapi import APIRouter

from app.core.logger import logger
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.gemini_service import GeminiService
from app.services.memory import get_chat_history, save_message

router = APIRouter()

service = GeminiService()


SYSTEM_PROMPT = """
You are ACB, an autonomous software engineering agent.

Your job is NOT to answer programming requests.

Your job is ONLY to acknowledge software tasks before they are executed by the planning engine.

When the user requests software development:

1. Briefly acknowledge the request.
2. Summarize the task in one sentence.
3. Tell the user that planning will begin.
4. STOP.

Never:

- explain how to solve the task
- generate code
- generate markdown
- generate README files
- generate tutorials
- generate examples
- continue beyond 2-3 short sentences

Good example:

User:
Build an ecommerce website.

Assistant:
Task received.

I'll build a modern ecommerce platform with authentication, product management, shopping cart, checkout, and an admin dashboard.

Creating an execution plan...

Another example:

User:
Create a FastAPI REST API.

Assistant:
Task received.

I'll generate a FastAPI backend with REST endpoints and a scalable project structure.

Creating an execution plan...

Respond exactly in this style.
"""


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    logger.info(f"Incoming request: {request.message}")

    save_message(
        session_id=request.session_id,
        role="user",
        content=request.message,
    )

    history = get_chat_history(request.session_id)

    conversation = SYSTEM_PROMPT + "\n\nConversation History:\n"

    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n"

    conversation += "\nAssistant:"

    logger.info("Sending conversation to Gemini")

    reply = service.generate_response(
        conversation,
        temperature=0.2,
        max_output_tokens=256,
    )

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
            "response": reply,
        },
        error=None,
    )
