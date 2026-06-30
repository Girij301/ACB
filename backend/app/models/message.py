from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, index=True)

    role = Column(String)

    content = Column(Text)

    timestamp = Column(DateTime, default=datetime.utcnow)