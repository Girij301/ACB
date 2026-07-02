from app.models.execution import Execution


def test_execution_creation():
    execution = Execution(
        session_id="session-1",
        plan_id=1,
        status="PENDING",
    )

    assert execution.session_id == "session-1"
    assert execution.plan_id == 1
    assert execution.status == "PENDING"
