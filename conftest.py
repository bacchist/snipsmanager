import pytest
import os


@pytest.fixture(autouse=True)
def good_string_body():
    name = "good_string_body.json"
    with open(name, "w") as f:
        f.write(
            '{"string of text": {"prefix": "str", "body": "just a string", "description": "that\'s it"}}'
        )
    yield
    os.remove(name)


@pytest.fixture(autouse=True)
def good_list_body():
    name = "good_list_body.json"
    with open(name, "w") as f:
        f.write(
            '{"list of stuff": {"prefix": "ls", "body": ["a line", "another line", "yet another line"], "description": "it\'s a list"}}'
        )
    yield
    os.remove(name)


@pytest.fixture(autouse=True)
def error_no_name():
    name = "error_no_name.json"
    with open(name, "w") as f:
        f.write(
            '{{"prefix": "pre", "body": "valid body", "description": "valid description"}}'
        )
    yield
    os.remove(name)


@pytest.fixture(autouse=True)
def warn_no_body():
    name = "warn_no_body.json"
    with open(name, "w") as f:
        f.write('{"nothing": {"prefix": "nada", "description": "nothing to see here"}}')
    yield
    os.remove(name)


@pytest.fixture(autouse=True)
def warn_no_prefix():
    name = "warn_no_prefix.json"
    with open(name, "w") as f:
        f.write('{"prefixless": {"body": "foobarbaz", "description": "whatever"}}')
    yield
    os.remove(name)


@pytest.fixture(autouse=True)
def warn_no_desc():
    name = "warn_no_desc.json"
    with open(name, "w") as f:
        f.write('{"no description": {"prefix": "nod", "body": "no description"}}')
    yield
    os.remove(name)


@pytest.fixture
def json_files():
    json_files = [
        "good_string_body.json",
        "good_list_body.json",
        "error_no_name.json",
        "warn_no_body.json",
        "warn_no_prefix.json",
        "warn_no_desc.json",
    ]
    return json_files
