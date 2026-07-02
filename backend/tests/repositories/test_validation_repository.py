from datetime import UTC, datetime

from app.core.database import Base
from app.models.execution import Execution
from app.models.validation_record import ValidationRecord
from app.repositories.validation_repository import ValidationRepository
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


def test_validation_repository_crud():
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

    repository = ValidationRepository(db)

    validation = ValidationRecord(
        execution_id=execution.id,
        validator_name="ruff",
        passed=True,
        stdout="No issues found",
        stderr="",
    )

    repository.create(validation)

    loaded = repository.get_by_id(validation.id)

    assert loaded is not None
    assert loaded.validator_name == "ruff"
    assert loaded.passed is True

    validations = repository.list_by_execution(execution.id)

    assert len(validations) == 1
    assert validations[0].validator_name == "ruff"

    repository.delete(validation)

    assert repository.list_by_execution(execution.id) == []

    db.close()
