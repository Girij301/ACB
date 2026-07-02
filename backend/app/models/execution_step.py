from datetime import UTC, datetime

from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class ExecutionStep(Base):
    __tablename__ = "execution_steps"

    id = Column(Integer, primary_key=True, index=True)

    execution_id = Column(
        Integer,
        ForeignKey("executions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    step_index = Column(Integer, nullable=False)

    action = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    status = Column(String, nullable=False)

    tool_name = Column(String, nullable=True)

    output = Column(Text, nullable=True)

    error = Column(Text, nullable=True)

    duration_ms = Column(Integer, default=0, nullable=False)

    started_at = Column(DateTime, nullable=False)

    completed_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    execution = relationship(
        "Execution",
        back_populates="execution_steps",
    )
