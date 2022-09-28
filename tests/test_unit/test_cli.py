import pytest
import pathlib
from typer.testing import CliRunner

from bulk.__main__ import app

runner = CliRunner()


@pytest.mark.parametrize("dataset", ["fruits", "pets", "twemoji"])
def test_download(dataset):
    result = runner.invoke(app, ["download", dataset])
    assert result.exit_code == 0
    assert pathlib.Path("downloads", dataset).exists()

    # The path exists now, so exit_code needs to be raised
    result = runner.invoke(app, ["download", dataset])
    assert result.exit_code == 1
