from datetime import UTC, datetime

from app.core.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship


class RetryRecord(Base):
    __tablename__ = "retry_records"

    id = Column(Integer, primary_key=True, index=True)

    execution_id = Column(
        Integer,
        ForeignKey("executions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    step_index = Column(Integer, nullable=False)

    attempt_number = Column(Integer, nullable=False)

    reason = Column(Text, nullable=False)

    previous_error = Column(Text, nullable=True)

    success = Column(Boolean, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    execution = relationship(
        "Execution",
        back_populates="retry_records",
    )