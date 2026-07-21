from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.message import Message


def save_message(
    db: Session,
    session_id: str,
    role: str,
    content: str,
):
    message = Message(
        session_id=session_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()


def get_chat_history(
    db: Session,
    session_id: str,
    limit: int = settings.MEMORY_LIMIT,
):
    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.timestamp.desc())
        .limit(limit)
        .all()
    )

    messages.reverse()

    return [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]