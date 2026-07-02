from unittest.mock import Mock

from app.services.execution_persistence_service import (
    ExecutionPersistenceService,
)


def test_execution_persistence_service_creation():
    service = ExecutionPersistenceService(
        execution_repository=Mock(),
        execution_step_repository=Mock(),
        validation_repository=Mock(),
        retry_repository=Mock(),
        debug_repository=Mock(),
    )

    assert service.execution_repository is not None
    assert service.execution_step_repository is not None
    assert service.validation_repository is not None
    assert service.retry_repository is not None
    assert service.debug_repository is not None