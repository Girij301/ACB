from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.core.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, index=True, nullable=False)

    user_task = Column(Text, nullable=False)

    plan = Column(Text, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
