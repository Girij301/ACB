from datetime import UTC, datetime

from app.core.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship


class DebugRecord(Base):
    __tablename__ = "debug_records"

    id = Column(Integer, primary_key=True, index=True)

    execution_id = Column(
        Integer,
        ForeignKey("executions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    step_index = Column(Integer, nullable=False)

    attempt_number = Column(Integer, nullable=False)

    failure_summary = Column(Text, nullable=False)

    ai_summary = Column(Text, nullable=True)

    success = Column(Boolean, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    execution = relationship(
        "Execution",
        back_populates="debug_records",
    )