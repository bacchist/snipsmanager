from typer.testing import CliRunner
from unittest.mock import ANY, patch

from project import app

runner = CliRunner()


def test_show_all(json_files):
    for json_file in json_files:
        result = runner.invoke(app, ["show-all", json_file])
        if json_file.startswith("error"):
            assert result.exit_code == 1
            assert "ERROR" in result.stdout
        elif json_file.startswith("warn"):
            assert result.exit_code == 0
            assert "WARNING" in result.stdout
            assert "Snippets from" in result.stdout
        else:
            assert result.exit_code == 0
            for alert in ["WARNING", "ERROR"]:
                assert alert not in result.stdout
            assert f"Snippets from {json_file}" in result.stdout


def test_show():
    result = runner.invoke(app, ["show", "good_string_body.json", "str"])
    assert result.exit_code == 0
    assert "just a string" in result.stdout

# TODO: Write tests for user input
def test_new(mocker):
    mock_run = mocker.patch("subprocess.call", return_value=0)
    result = runner.invoke(
        app,
        ["new", "good_string_body.json"],
        input="somename\nsomeprefix\na description\n",
    )
    assert "Snippet's name" in result.stdout
    mock_run.assert_called_once_with(["nvim", ANY])
    assert result.exit_code == 0


def test_edit(mocker):
    mock_run = mocker.patch("subprocess.call")
    result = runner.invoke(app, ["edit", "good_string_body.json", "str"])
    mock_run.assert_called_once_with(["nvim", ANY])
    assert result.exit_code == 0
