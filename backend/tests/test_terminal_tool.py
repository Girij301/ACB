import pytest
from app.tools.terminal_tool import TerminalTool

tool = TerminalTool()


def test_python_version():
    result = tool.run("python --version")

    assert result["success"] is True
    assert result["exit_code"] == 0
    assert "Python" in result["stdout"] or "Python" in result["stderr"]


def test_invalid_command():
    result = tool.run("command_that_does_not_exist")

    assert result["success"] is False
    assert result["exit_code"] != 0


def test_timeout():
    result = tool.run(
        "ping 127.0.0.1 -n 100",
        timeout=2,
    )

    assert result["success"] is False
    assert "timed out" in result["stderr"].lower()


def test_invalid_directory():

    with pytest.raises(FileNotFoundError):
        tool.run(
            "python --version",
            cwd="directory_that_does_not_exist",
        )


def test_directory_traversal():

    with pytest.raises(ValueError):
        tool.run(
            "python --version",
            cwd="../../",
        )


def test_stdout_capture():
    result = tool.run("python --version")

    assert len(result["stdout"]) > 0 or len(result["stderr"]) > 0


def test_exit_code():
    success = tool.run("python --version")
    failure = tool.run("command_that_does_not_exist")

    assert success["exit_code"] == 0
    assert failure["exit_code"] != 0
