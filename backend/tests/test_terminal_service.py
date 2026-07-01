from app.services.terminal_service import TerminalService

service = TerminalService()


def test_execute_command():
    result = service.execute_command("python --version")

    assert result["success"] is True
    assert result["exit_code"] == 0
