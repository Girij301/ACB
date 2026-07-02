from datetime import UTC, datetime

from app.core.database import Base
from app.models.execution import Execution
from app.models.execution_step import ExecutionStep
from app.repositories.execution_step_repository import ExecutionStepRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


def test_execution_step_repository_crud():
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

    repository = ExecutionStepRepository(db)

    step_one = ExecutionStep(
        execution_id=execution.id,
        step_index=1,
        action="CREATE_FILE",
        description="Create main.py",
        status="SUCCESS",
        tool_name="FileTool",
        output="Created",
        error=None,
        started_at=datetime.now(UTC),
    )

    step_two = ExecutionStep(
        execution_id=execution.id,
        step_index=2,
        action="RUN_COMMAND",
        description="Run compile",
        status="SUCCESS",
        tool_name="TerminalTool",
        output="OK",
        error=None,
        started_at=datetime.now(UTC),
    )

    repository.create(step_one)
    repository.create(step_two)

    steps = repository.list_by_execution(execution.id)

    assert len(steps) == 2
    assert steps[0].step_index == 1
    assert steps[1].step_index == 2

    loaded = repository.get_by_id(step_one.id)

    assert loaded is not None
    assert loaded.description == "Create main.py"

    repository.delete(step_one)

    remaining = repository.list_by_execution(execution.id)

    assert len(remaining) == 1
    assert remaining[0].step_index == 2

    db.close()
