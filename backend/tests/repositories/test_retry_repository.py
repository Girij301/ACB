from datetime import UTC, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.execution import Execution
from app.models.retry_record import RetryRecord
from app.repositories.retry_repository import RetryRepository

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def setup_function():
    Base.metadata.create_all(bind=engine)


def teardown_function():
    Base.metadata.drop_all(bind=engine)


def test_retry_repository_crud():
    db = TestingSessionLocal()

    execution = Execution(
        session_id="session-1",
        plan_id=1,
        status="RUNNING",
        started_at=datetime.now(UTC),
    )

    db.add(execution)
    db.commit()
    db.refresh(execution)

    repository = RetryRepository(db)

    retry = RetryRecord(
        execution_id=execution.id,
        step_index=1,
        attempt_number=1,
        reason="Command failed",
        previous_error="Exit code 1",
        success=True,
    )

    repository.create(retry)

    loaded = repository.get_by_id(retry.id)

    assert loaded is not None
    assert loaded.attempt_number == 1
    assert loaded.success is True

    retries = repository.list_by_execution(execution.id)

    assert len(retries) == 1
    assert retries[0].reason == "Command failed"

    repository.delete(retry)

    assert repository.list_by_execution(execution.id) == []

    db.close()