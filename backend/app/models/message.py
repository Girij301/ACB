from datetime import UTC, datetime

from app.core.database import Base
from sqlalchemy import Column, DateTime, Integer, String, Text


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, index=True)

    role = Column(String)

    content = Column(Text)

    timestamp = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
    )

