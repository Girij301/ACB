from app.core.config import settings
from app.core.database import SessionLocal
from app.models.message import Message


# Save a user or assistant message to the database.
def save_message(session_id: str, role: str, content: str):

    db = SessionLocal()

    try:
        message = Message(
            session_id=session_id,
            role=role,
            content=content,
        )

        db.add(message)
        db.commit()

    finally:
        db.close()


# Retrieve all messages for a specific conversation session./most recent


def get_chat_history(session_id: str, limit: int = settings.MEMORY_LIMIT):
    db = SessionLocal()

    try:
        messages = (
            db.query(Message)
            .filter(Message.session_id == session_id)
            .order_by(Message.timestamp.desc())
            .limit(limit)
            .all()
        )

        # Return oldest message first
        messages.reverse()

        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

    finally:
        db.close()
