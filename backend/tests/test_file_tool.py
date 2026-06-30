import shutil

from app.tools.file_tool import FileTool, get_safe_path

tool = FileTool()


def test_create_file():
    path = "pytest/create.txt"

    if tool.exists(path):
        tool.delete_file(path)

    tool.create_file(path, "Hello")

    assert tool.exists(path)


def test_read_file():
    path = "pytest/read.txt"

    if tool.exists(path):
        tool.delete_file(path)

    tool.create_file(path, "Hello World")

    content = tool.read_file(path)

    assert content == "Hello World"


def test_write_file():
    path = "pytest/write.txt"

    if tool.exists(path):
        tool.delete_file(path)

    tool.create_file(path, "Old")

    tool.write_file(path, "New")

    assert tool.read_file(path) == "New"


def test_append_file():
    path = "pytest/append.txt"

    if tool.exists(path):
        tool.delete_file(path)

    tool.create_file(path, "Hello")

    tool.append_file(path, " World")

    assert tool.read_file(path) == "Hello World"


def test_delete_file():
    path = "pytest/delete.txt"

    if tool.exists(path):
        tool.delete_file(path)

    tool.create_file(path)

    tool.delete_file(path)

    assert not tool.exists(path)


def test_create_directory():
    path = "pytest/my_folder"

    if tool.exists(path):
        shutil.rmtree(get_safe_path(path), ignore_errors=True)

    tool.create_directory(path)

    assert tool.exists(path)


def test_exists():
    path = "pytest/exists.txt"

    if tool.exists(path):
        tool.delete_file(path)

    tool.create_file(path)

    assert tool.exists(path)
