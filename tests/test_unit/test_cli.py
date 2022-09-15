import pathlib 
from typer.testing import CliRunner

from bulk.__main__ import app

runner = CliRunner()
 

def test_download_tinyplanet():
    result = runner.invoke(app, ["util", "download", "tinyplanet"])
    assert result.exit_code == 0
    assert pathlib.Path("downloads/tinyplanet").exists()

    # The path exists now, so exit_code needs to be raised
    result = runner.invoke(app, ["util", "download", "tinyplanet"])
    assert result.exit_code == 1
