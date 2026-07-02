from datetime import datetime

from app.core.database import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship


class Execution(Base):
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        String,
        index=True,
        nullable=False,
    )

    plan_id = Column(
        Integer,
        index=True,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
    )

    started_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    completed_at = Column(
        DateTime,
        nullable=True,
    )

    duration_ms = Column(
        Integer,
        default=0,
        nullable=False,
    )

    total_steps = Column(
        Integer,
        default=0,
        nullable=False,
    )

    successful_steps = Column(
        Integer,
        default=0,
        nullable=False,
    )

    failed_steps = Column(
        Integer,
        default=0,
        nullable=False,
    )

    retry_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    debug_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    validation_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    execution_steps = relationship(
        "ExecutionStep",
        back_populates="execution",
        cascade="all, delete-orphan",
    )

    validation_records = relationship(
        "ValidationRecord",
        back_populates="execution",
        cascade="all, delete-orphan",
    )

    retry_records = relationship(
        "RetryRecord",
        back_populates="execution",
        cascade="all, delete-orphan",
    )

    debug_records = relationship(
        "DebugRecord",
        back_populates="execution",
        cascade="all, delete-orphan",
    )