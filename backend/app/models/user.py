from datetime import UTC, datetime

from app.core.database import Base
from sqlalchemy import Column, DateTime, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    clerk_user_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    first_name = Column(
        String,
        nullable=True,
    )

    last_name = Column(
        String,
        nullable=True,
    )

    image_url = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
