from app.schemas.execution_status import ExecutionStatus, StepStatus


def test_execution_status_values():
    assert ExecutionStatus.PENDING.value == "PENDING"
    assert ExecutionStatus.RUNNING.value == "RUNNING"
    assert ExecutionStatus.SUCCESS.value == "SUCCESS"
    assert ExecutionStatus.FAILED.value == "FAILED"
    assert ExecutionStatus.CANCELLED.value == "CANCELLED"


def test_step_status_values():
    assert StepStatus.PENDING.value == "PENDING"
    assert StepStatus.RUNNING.value == "RUNNING"
    assert StepStatus.SUCCESS.value == "SUCCESS"
    assert StepStatus.FAILED.value == "FAILED"
    assert StepStatus.SKIPPED.value == "SKIPPED"
