from unittest.mock import Mock

from app.docker.execution_container import ExecutionContainer

def test_execution_container_create():
    docker_manager = Mock()

    fake_container = Mock()
    fake_container.id = "container-123"

    docker_manager.create_container.return_value = fake_container

    container = ExecutionContainer(
        docker_manager=docker_manager,
        config=Mock(),
    )

    container.create()

    docker_manager.create_container.assert_called_once()

    assert container.container == fake_container
    assert container.id == "container-123"

def test_execution_container_start():
    docker_manager = Mock()

    fake_container = Mock()
    fake_container.id = "container-123"

    docker_manager.create_container.return_value = fake_container

    container = ExecutionContainer(
        docker_manager=docker_manager,
        config=Mock(),
    )

    container.create()
    container.start()

    docker_manager.start_container.assert_called_once_with(
        "container-123"
    )

def test_execution_container_execute():
    docker_manager = Mock()

    fake_container = Mock()
    fake_container.id = "container-123"

    docker_manager.create_container.return_value = fake_container

    expected_result = Mock()
    docker_manager.exec_run.return_value = expected_result

    container = ExecutionContainer(
        docker_manager=docker_manager,
        config=Mock(),
    )

    container.create()

    result = container.execute(
        command="ls",
        cwd="/workspace",
    )

    docker_manager.exec_run.assert_called_once_with(
        container_id="container-123",
        command="ls",
        cwd="/workspace",
    )

    assert result == expected_result

def test_execution_container_close():
    docker_manager = Mock()

    fake_container = Mock()
    fake_container.id = "container-123"

    docker_manager.create_container.return_value = fake_container

    container = ExecutionContainer(
        docker_manager=docker_manager,
        config=Mock(),
    )

    container.create()
    container.close()

    docker_manager.stop_container.assert_called_once_with(
        "container-123"
    )

    docker_manager.remove_container.assert_called_once_with(
        "container-123",
        force=True,
    )

def test_execution_container_close_without_create():
    docker_manager = Mock()

    container = ExecutionContainer(
        docker_manager=docker_manager,
        config=Mock(),
    )

    container.close()

    docker_manager.stop_container.assert_not_called()
    docker_manager.remove_container.assert_not_called()

