from typer.testing import CliRunner

from filet.__main__ import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


# def test_config():
#     result = runner.invoke(app, ["config", "--help"])
#     assert result.exit_code == 0
#     result = runner.invoke(config_group, ["--help"])
