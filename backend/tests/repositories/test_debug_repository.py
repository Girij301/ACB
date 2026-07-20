from datetime import UTC, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.models.debug_record import DebugRecord
from app.models.execution import Execution
from app.repositories.debug_repository import DebugRepository

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


def test_debug_repository_crud():
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

    repository = DebugRepository(db)

    debug = DebugRecord(
        execution_id=execution.id,
        step_index=1,
        attempt_number=1,
        failure_summary="Compilation failed",
        ai_summary="Added missing import",
        success=True,
    )

    repository.create(debug)

    loaded = repository.get_by_id(debug.id)

    assert loaded is not None
    assert loaded.ai_summary == "Added missing import"
    assert loaded.success is True

    records = repository.list_by_execution(execution.id)

    assert len(records) == 1
    assert records[0].failure_summary == "Compilation failed"

    repository.delete(debug)

    assert repository.list_by_execution(execution.id) == []

    db.close()
